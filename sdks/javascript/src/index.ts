// ────────────────────────────────────────────────────────────────────────────
// PayChains JavaScript/TypeScript SDK
// ────────────────────────────────────────────────────────────────────────────

const DEFAULT_BASE_URL = "https://api.paychains.dev/api/v1";

// ── Configuration ───────────────────────────────────────────────────────────

export interface PayChainsConfig {
  /** Your PayChains API key. */
  apiKey: string;
  /** Override the default API base URL. */
  baseUrl?: string;
}

// ── Request / Response helpers ──────────────────────────────────────────────

export interface PaginatedResponse<T> {
  data: T[];
  page: number;
  per_page: number;
  total: number;
}

export interface PaginationParams {
  page?: number;
  per_page?: number;
}

// ── Domain types ────────────────────────────────────────────────────────────

export interface PaymentCreateParams {
  amount_usd: number;
  token: string;
  chain: string;
  metadata?: Record<string, unknown>;
  payment_link_id?: string;
}

export interface Payment {
  id: string;
  status: string;
  amount_usd: string;
  amount_crypto: string | null;
  token: string;
  chain: string;
  deposit_address: string;
  tx_hash: string | null;
  confirmations: number;
  required_confirmations: number;
  expires_at: string;
  created_at: string;
}

export interface PaymentListParams extends PaginationParams {
  status?: string;
  chain?: string;
}

export interface PaymentLinkCreateParams {
  title: string;
  description?: string;
  amount_usd?: number;
}

export interface PaymentLink {
  id: string;
  title: string;
  description: string | null;
  amount_usd: number | null;
  is_active: boolean;
  created_at: string;
}

export interface SubscriptionCreateParams {
  plan_name: string;
  amount_usd: number;
  interval: string;
  token: string;
  chain: string;
  metadata?: Record<string, unknown>;
}

export interface Subscription {
  id: string;
  plan_name: string;
  amount_usd: number;
  interval: string;
  status: string;
  next_payment_at: string;
  created_at: string;
}

export interface WebhookEvent {
  id: string;
  event_type: string;
  payload: Record<string, unknown>;
  status: string;
  created_at: string;
}

export interface PayoutRequestParams {
  amount: number;
  token: string;
  chain: string;
  to_address: string;
}

export interface Payout {
  id: string;
  amount: string;
  token: string;
  chain: string;
  status: string;
  tx_hash: string | null;
  created_at: string;
}

export interface AnalyticsOverview {
  total_payments: number;
  total_volume_usd: string;
  successful_payments: number;
  failed_payments: number;
  period_days: number;
}

export interface AnalyticsByChain {
  chain: string;
  total_payments: number;
  total_volume_usd: string;
}

export interface AnalyticsByToken {
  token: string;
  total_payments: number;
  total_volume_usd: string;
}

// ── Error class ─────────────────────────────────────────────────────────────

export class PayChainsError extends Error {
  public readonly status: number;
  public readonly body: unknown;

  constructor(message: string, status: number, body: unknown) {
    super(message);
    this.name = "PayChainsError";
    this.status = status;
    this.body = body;
  }
}

// ── HMAC-SHA256 (synchronous, pure-JS) ─────────────────────────────────────
//
// We provide a self-contained HMAC-SHA256 so webhook signature verification
// works synchronously in any runtime without external dependencies.

function sha256(data: Uint8Array): Uint8Array {
  // SHA-256 constants
  const K: number[] = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
  ];

  let h0 = 0x6a09e667;
  let h1 = 0xbb67ae85;
  let h2 = 0x3c6ef372;
  let h3 = 0xa54ff53a;
  let h4 = 0x510e527f;
  let h5 = 0x9b05688c;
  let h6 = 0x1f83d9ab;
  let h7 = 0x5be0cd19;

  // Pre-processing: add padding
  const bitLen = data.length * 8;
  // message + 1 byte (0x80) + padding + 8 bytes length
  const totalLen = Math.ceil((data.length + 9) / 64) * 64;
  const padded = new Uint8Array(totalLen);
  padded.set(data);
  padded[data.length] = 0x80;
  // Append length as 64-bit big-endian (we only handle up to 2^32 bits)
  const view = new DataView(padded.buffer);
  view.setUint32(totalLen - 4, bitLen, false);

  const w = new Int32Array(64);

  for (let offset = 0; offset < totalLen; offset += 64) {
    for (let i = 0; i < 16; i++) {
      w[i] = view.getInt32(offset + i * 4, false);
    }
    for (let i = 16; i < 64; i++) {
      const s0 =
        (((w[i - 15]!) >>> 7) | ((w[i - 15]!) << 25)) ^
        (((w[i - 15]!) >>> 18) | ((w[i - 15]!) << 14)) ^
        ((w[i - 15]!) >>> 3);
      const s1 =
        (((w[i - 2]!) >>> 17) | ((w[i - 2]!) << 15)) ^
        (((w[i - 2]!) >>> 19) | ((w[i - 2]!) << 13)) ^
        ((w[i - 2]!) >>> 10);
      w[i] = (w[i - 16]! + s0 + w[i - 7]! + s1) | 0;
    }

    let a = h0, b = h1, c = h2, d = h3;
    let e = h4, f = h5, g = h6, h = h7;

    for (let i = 0; i < 64; i++) {
      const S1 =
        (((e) >>> 6) | ((e) << 26)) ^
        (((e) >>> 11) | ((e) << 21)) ^
        (((e) >>> 25) | ((e) << 7));
      const ch = (e & f) ^ (~e & g);
      const temp1 = (h + S1 + ch + K[i]! + w[i]!) | 0;
      const S0 =
        (((a) >>> 2) | ((a) << 30)) ^
        (((a) >>> 13) | ((a) << 19)) ^
        (((a) >>> 22) | ((a) << 10));
      const maj = (a & b) ^ (a & c) ^ (b & c);
      const temp2 = (S0 + maj) | 0;

      h = g; g = f; f = e;
      e = (d + temp1) | 0;
      d = c; c = b; b = a;
      a = (temp1 + temp2) | 0;
    }

    h0 = (h0 + a) | 0;
    h1 = (h1 + b) | 0;
    h2 = (h2 + c) | 0;
    h3 = (h3 + d) | 0;
    h4 = (h4 + e) | 0;
    h5 = (h5 + f) | 0;
    h6 = (h6 + g) | 0;
    h7 = (h7 + h) | 0;
  }

  const result = new Uint8Array(32);
  const rv = new DataView(result.buffer);
  rv.setInt32(0, h0, false);
  rv.setInt32(4, h1, false);
  rv.setInt32(8, h2, false);
  rv.setInt32(12, h3, false);
  rv.setInt32(16, h4, false);
  rv.setInt32(20, h5, false);
  rv.setInt32(24, h6, false);
  rv.setInt32(28, h7, false);
  return result;
}

function hmacSha256(key: Uint8Array, message: Uint8Array): Uint8Array {
  const BLOCK_SIZE = 64;

  // If key is longer than block size, hash it first
  let k = key.length > BLOCK_SIZE ? sha256(key) : key;

  // Pad key to block size
  const paddedKey = new Uint8Array(BLOCK_SIZE);
  paddedKey.set(k);

  const ipad = new Uint8Array(BLOCK_SIZE);
  const opad = new Uint8Array(BLOCK_SIZE);
  for (let i = 0; i < BLOCK_SIZE; i++) {
    ipad[i] = paddedKey[i]! ^ 0x36;
    opad[i] = paddedKey[i]! ^ 0x5c;
  }

  // inner hash: H(ipad || message)
  const inner = new Uint8Array(BLOCK_SIZE + message.length);
  inner.set(ipad);
  inner.set(message, BLOCK_SIZE);
  const innerHash = sha256(inner);

  // outer hash: H(opad || innerHash)
  const outer = new Uint8Array(BLOCK_SIZE + 32);
  outer.set(opad);
  outer.set(innerHash, BLOCK_SIZE);
  return sha256(outer);
}

function toHex(bytes: Uint8Array): string {
  let hex = "";
  for (let i = 0; i < bytes.length; i++) {
    hex += bytes[i]!.toString(16).padStart(2, "0");
  }
  return hex;
}

function textToBytes(text: string): Uint8Array {
  if (typeof TextEncoder !== "undefined") {
    return new TextEncoder().encode(text);
  }
  // Fallback for environments without TextEncoder
  const bytes: number[] = [];
  for (let i = 0; i < text.length; i++) {
    const code = text.charCodeAt(i);
    if (code < 0x80) {
      bytes.push(code);
    } else if (code < 0x800) {
      bytes.push(0xc0 | (code >> 6), 0x80 | (code & 0x3f));
    } else {
      bytes.push(
        0xe0 | (code >> 12),
        0x80 | ((code >> 6) & 0x3f),
        0x80 | (code & 0x3f),
      );
    }
  }
  return new Uint8Array(bytes);
}

/**
 * Compute an HMAC-SHA256 hex digest synchronously.
 */
function computeHmacHex(key: string, message: string): string {
  return toHex(hmacSha256(textToBytes(key), textToBytes(message)));
}

/**
 * Constant-time string comparison to prevent timing attacks.
 */
function timingSafeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let result = 0;
  for (let i = 0; i < a.length; i++) {
    result |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return result === 0;
}

// ── Query string helper ────────────────────────────────────────────────────

function toQueryString(params: Record<string, unknown> | object): string {
  const parts: string[] = [];
  for (const [key, value] of Object.entries(params as Record<string, unknown>)) {
    if (value !== undefined && value !== null) {
      parts.push(`${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`);
    }
  }
  return parts.length > 0 ? `?${parts.join("&")}` : "";
}

// ── Main client class ──────────────────────────────────────────────────────

export class PayChains {
  private readonly apiKey: string;
  private readonly baseUrl: string;

  constructor(config: PayChainsConfig) {
    if (!config.apiKey) {
      throw new Error("PayChains: apiKey is required");
    }
    this.apiKey = config.apiKey;
    this.baseUrl = (config.baseUrl ?? DEFAULT_BASE_URL).replace(/\/+$/, "");
  }

  // ── Internal request method ─────────────────────────────────────────────

  private async request<T>(
    method: string,
    endpoint: string,
    body?: unknown,
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const headers: Record<string, string> = {
      "X-API-Key": this.apiKey,
      "Accept": "application/json",
    };

    const init: RequestInit = { method, headers };

    if (body !== undefined) {
      headers["Content-Type"] = "application/json";
      init.body = JSON.stringify(body);
    }

    const response = await fetch(url, init);

    let responseBody: unknown;
    const contentType = response.headers.get("content-type") ?? "";
    if (contentType.includes("application/json")) {
      responseBody = await response.json();
    } else {
      responseBody = await response.text();
    }

    if (!response.ok) {
      const message =
        typeof responseBody === "object" &&
        responseBody !== null &&
        "message" in responseBody
          ? String((responseBody as Record<string, unknown>).message)
          : `Request failed with status ${response.status}`;
      throw new PayChainsError(message, response.status, responseBody);
    }

    return responseBody as T;
  }

  // ── Payments ────────────────────────────────────────────────────────────

  payments = {
    /**
     * Create a new payment.
     */
    create: (params: PaymentCreateParams): Promise<Payment> =>
      this.request<Payment>("POST", "/payments/create", params),

    /**
     * Retrieve a payment by ID.
     */
    get: (id: string): Promise<Payment> =>
      this.request<Payment>("GET", `/payments/${encodeURIComponent(id)}`),

    /**
     * List payments with optional filters.
     */
    list: (params?: PaymentListParams): Promise<PaginatedResponse<Payment>> =>
      this.request<PaginatedResponse<Payment>>(
        "GET",
        `/payments${toQueryString(params ?? {})}`,
      ),

    /**
     * Refund a payment.
     */
    refund: (id: string): Promise<Payment> =>
      this.request<Payment>(
        "POST",
        `/payments/${encodeURIComponent(id)}/refund`,
      ),
  };

  // ── Payment Links ──────────────────────────────────────────────────────

  paymentLinks = {
    /**
     * Create a new payment link.
     */
    create: (params: PaymentLinkCreateParams): Promise<PaymentLink> =>
      this.request<PaymentLink>("POST", "/payment-links", params),

    /**
     * List all payment links.
     */
    list: (): Promise<PaymentLink[]> =>
      this.request<PaymentLink[]>("GET", "/payment-links"),
  };

  // ── Subscriptions ──────────────────────────────────────────────────────

  subscriptions = {
    /**
     * Create a new subscription.
     */
    create: (params: SubscriptionCreateParams): Promise<Subscription> =>
      this.request<Subscription>("POST", "/subscriptions", params),

    /**
     * List all subscriptions.
     */
    list: (): Promise<Subscription[]> =>
      this.request<Subscription[]>("GET", "/subscriptions"),
  };

  // ── Webhooks ───────────────────────────────────────────────────────────

  webhooks = {
    /**
     * List recent webhook events.
     */
    listEvents: (): Promise<WebhookEvent[]> =>
      this.request<WebhookEvent[]>("GET", "/webhooks/events"),

    /**
     * Send a test webhook event.
     */
    sendTest: (): Promise<{ success: boolean }> =>
      this.request<{ success: boolean }>("POST", "/webhooks/test"),

    /**
     * Verify a webhook signature (synchronous, pure-JS HMAC-SHA256).
     *
     * @param payload  - The raw request body string.
     * @param signature - The signature from the `X-PayChains-Signature` header.
     * @param secret   - Your webhook signing secret.
     * @returns `true` if the signature is valid.
     */
    verifySignature: (
      payload: string,
      signature: string,
      secret: string,
    ): boolean => {
      const expected = computeHmacHex(secret, payload);
      return timingSafeEqual(expected, signature.toLowerCase());
    },
  };

  // ── Payouts ────────────────────────────────────────────────────────────

  payouts = {
    /**
     * List all payouts.
     */
    list: (): Promise<Payout[]> =>
      this.request<Payout[]>("GET", "/payouts"),

    /**
     * Request a new payout.
     */
    request: (params: PayoutRequestParams): Promise<Payout> =>
      this.request<Payout>("POST", "/payouts", params),
  };

  // ── Analytics ──────────────────────────────────────────────────────────

  analytics = {
    /**
     * Get an overview of payment analytics.
     */
    overview: (params?: { days?: number }): Promise<AnalyticsOverview> =>
      this.request<AnalyticsOverview>(
        "GET",
        `/analytics/overview${toQueryString(params ?? {})}`,
      ),

    /**
     * Get analytics grouped by chain.
     */
    byChain: (): Promise<AnalyticsByChain[]> =>
      this.request<AnalyticsByChain[]>("GET", "/analytics/by-chain"),

    /**
     * Get analytics grouped by token.
     */
    byToken: (): Promise<AnalyticsByToken[]> =>
      this.request<AnalyticsByToken[]>("GET", "/analytics/by-token"),
  };
}

export default PayChains;
