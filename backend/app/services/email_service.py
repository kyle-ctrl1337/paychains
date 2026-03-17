"""Email service using Resend for transactional emails."""

import logging
import resend
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _init_resend():
    if settings.resend_api_key:
        resend.api_key = settings.resend_api_key


def send_payment_receipt(to_email: str, payment_data: dict):
    """Send a payment receipt email."""
    _init_resend()
    if not settings.resend_api_key:
        logger.warning("Resend API key not configured, skipping email")
        return

    try:
        resend.Emails.send({
            "from": f"PayChains <{settings.from_email}>",
            "to": [to_email],
            "subject": f"Payment Confirmed — {payment_data.get('amount_usd', '')} USD",
            "html": f"""
            <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #7c3aed;">PayChains</h2>
                <p>Your payment has been confirmed.</p>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Amount</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #eee;">${payment_data.get('amount_usd', '0')} USD</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Token</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #eee;">{payment_data.get('token', '')}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Chain</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #eee;">{payment_data.get('chain', '')}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>TX Hash</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #eee; font-family: monospace; font-size: 12px;">{payment_data.get('tx_hash', 'N/A')}</td></tr>
                </table>
                <p style="color: #666; font-size: 14px; margin-top: 24px;">
                    Powered by <a href="https://paychains.dev" style="color: #7c3aed;">PayChains</a>
                </p>
            </div>
            """,
        })
        logger.info(f"Payment receipt sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")


def send_subscription_invoice(to_email: str, subscription_data: dict):
    """Send a subscription payment due notification."""
    _init_resend()
    if not settings.resend_api_key:
        return

    try:
        resend.Emails.send({
            "from": f"PayChains <{settings.from_email}>",
            "to": [to_email],
            "subject": f"Payment Due — {subscription_data.get('plan_name', 'Subscription')}",
            "html": f"""
            <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #7c3aed;">PayChains</h2>
                <p>Your subscription payment is due.</p>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Plan</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #eee;">{subscription_data.get('plan_name', '')}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Amount</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #eee;">${subscription_data.get('amount_usd', '0')} USD</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Due Date</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #eee;">{subscription_data.get('due_date', '')}</td></tr>
                </table>
                <p>Please send payment within 48 hours to keep your subscription active.</p>
                <p style="color: #666; font-size: 14px; margin-top: 24px;">
                    Powered by <a href="https://paychains.dev" style="color: #7c3aed;">PayChains</a>
                </p>
            </div>
            """,
        })
        logger.info(f"Subscription invoice sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
