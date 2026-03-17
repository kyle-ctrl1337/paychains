"""EVM chain provider — supports Ethereum, Polygon, BSC, Arbitrum, Base."""

import json
import logging
from decimal import Decimal

from web3 import AsyncWeb3, AsyncHTTPProvider
from web3.exceptions import TransactionNotFound

from app.blockchain.base import ChainProvider, Transaction

logger = logging.getLogger(__name__)

CHAIN_CONFIRMATIONS = {
    "ethereum": 3,
    "polygon": 5,
    "bsc": 5,
    "arbitrum": 1,
    "base": 1,
}

# ERC-20 Transfer event topic
TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

# ERC-20 token contract addresses (mainnet)
TOKEN_CONTRACTS = {
    "ethereum": {
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    },
    "polygon": {
        "USDC": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
        "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
    },
    "bsc": {
        "USDC": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
        "USDT": "0x55d398326f99059fF775485246999027B3197955",
    },
    "arbitrum": {
        "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
    },
    "base": {
        "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    },
}

TOKEN_DECIMALS = {
    "USDC": 6, "USDT": 6, "DAI": 18,
    "ETH": 18, "MATIC": 18, "BNB": 18,
}

NATIVE_TOKENS = {"ETH", "MATIC", "BNB"}

ERC20_ABI = json.loads(
    '[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],'
    '"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]'
)


class EVMProvider(ChainProvider):
    """Provider for EVM-compatible chains."""

    def __init__(self, chain: str, rpc_url: str):
        self.chain = chain.lower()
        self.rpc_url = rpc_url.replace("wss://", "https://").replace("ws://", "http://")
        self.required_confs = CHAIN_CONFIRMATIONS.get(self.chain, 3)
        self._w3: AsyncWeb3 | None = None

    def _get_web3(self) -> AsyncWeb3:
        if self._w3 is None:
            if not self.rpc_url:
                raise ConnectionError(f"No RPC URL configured for {self.chain}")
            self._w3 = AsyncWeb3(AsyncHTTPProvider(self.rpc_url))
        return self._w3

    async def generate_address(self, seed: bytes, account_index: int, address_index: int) -> str:
        from app.blockchain.wallet import derive_evm_address
        address, _ = derive_evm_address(seed, account_index, address_index)
        return address

    async def get_balance(self, address: str, token: str | None = None) -> Decimal:
        w3 = self._get_web3()
        addr = AsyncWeb3.to_checksum_address(address)

        if token is None or token.upper() in NATIVE_TOKENS:
            balance_wei = await w3.eth.get_balance(addr)
            return Decimal(balance_wei) / Decimal(10**18)

        # ERC-20
        chain_contracts = TOKEN_CONTRACTS.get(self.chain, {})
        contract_addr = chain_contracts.get(token.upper())
        if not contract_addr:
            raise ValueError(f"Token {token} not supported on {self.chain}")

        contract = w3.eth.contract(
            address=AsyncWeb3.to_checksum_address(contract_addr), abi=ERC20_ABI
        )
        balance = await contract.functions.balanceOf(addr).call()
        decimals = TOKEN_DECIMALS.get(token.upper(), 18)
        return Decimal(balance) / Decimal(10**decimals)

    async def get_transaction(self, tx_hash: str) -> Transaction | None:
        w3 = self._get_web3()
        try:
            tx = await w3.eth.get_transaction(tx_hash)
            current_block = await w3.eth.block_number
            confs = (current_block - tx["blockNumber"]) if tx.get("blockNumber") else 0
            return Transaction(
                tx_hash=tx_hash,
                from_address=tx["from"],
                to_address=tx.get("to", ""),
                amount=Decimal(tx["value"]) / Decimal(10**18),
                token="native",
                block_number=tx.get("blockNumber", 0),
                confirmations=confs,
            )
        except (TransactionNotFound, Exception):
            return None

    async def get_confirmations(self, tx_hash: str) -> int:
        w3 = self._get_web3()
        try:
            tx = await w3.eth.get_transaction(tx_hash)
            if not tx.get("blockNumber"):
                return 0
            current_block = await w3.eth.block_number
            return current_block - tx["blockNumber"]
        except Exception:
            return 0

    async def check_erc20_transfers(self, address: str, token: str, from_block: int) -> list[dict]:
        """Check for ERC-20 Transfer events to a given address since from_block."""
        w3 = self._get_web3()
        chain_contracts = TOKEN_CONTRACTS.get(self.chain, {})
        contract_addr = chain_contracts.get(token.upper())
        if not contract_addr:
            return []

        addr = AsyncWeb3.to_checksum_address(address)
        padded = "0x" + addr[2:].lower().zfill(64)

        try:
            logs = await w3.eth.get_logs({
                "address": AsyncWeb3.to_checksum_address(contract_addr),
                "topics": [TRANSFER_TOPIC, None, padded],
                "fromBlock": from_block,
            })

            transfers = []
            decimals = TOKEN_DECIMALS.get(token.upper(), 18)
            for log in logs:
                amount_raw = int(log["data"], 16) if isinstance(log["data"], str) else int.from_bytes(log["data"], "big")
                transfers.append({
                    "tx_hash": log["transactionHash"].hex() if isinstance(log["transactionHash"], bytes) else log["transactionHash"],
                    "from_address": "0x" + log["topics"][1].hex()[-40:] if isinstance(log["topics"][1], bytes) else "0x" + log["topics"][1][-40:],
                    "to_address": address,
                    "amount": Decimal(amount_raw) / Decimal(10**decimals),
                    "block_number": log["blockNumber"],
                    "token": token.upper(),
                })
            return transfers
        except Exception as e:
            logger.error(f"Error checking ERC-20 transfers on {self.chain}: {e}")
            return []

    async def subscribe_address(self, address: str, callback):
        pass  # Polling-based monitoring used instead — see monitor_tasks.py

    def get_required_confirmations(self) -> int:
        return self.required_confs
