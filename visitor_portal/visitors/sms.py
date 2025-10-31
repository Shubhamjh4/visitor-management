import os
import re
from typing import Optional
import json
import urllib.request
import urllib.error


def _normalize_phone(raw: str, default_country: str = "IN") -> Optional[str]:
    """Return E.164 phone or None if cannot normalize.

    Current logic favors India (+91):
    - Accepts +E164 as-is (digits only after '+').
    - Strips spaces/dashes/parentheses.
    - If starts with '0', trim leading zeros.
    - If 10 digits, assume Indian local and prefix +91.
    - If starts with 91 and total 12 digits, prefix '+'.
    - Basic length guard: 10..15 digits after country code.
    """
    if not raw:
        return None
    s = str(raw).strip()
    # Keep leading +, remove other non-digits
    if s.startswith('+'):
        digits = '+' + re.sub(r"\D", "", s[1:])
        # Must be + followed by 10-15 digits
        if re.fullmatch(r"\+[0-9]{10,15}", digits):
            return digits
        return None

    # Remove all non-digits
    digits_only = re.sub(r"\D", "", s)
    if not digits_only:
        return None

    # Trim leading zeros
    digits_only = digits_only.lstrip('0') or '0'

    # India heuristics
    if default_country.upper() == 'IN':
        if len(digits_only) == 10:
            return "+91" + digits_only
        if digits_only.startswith('91') and len(digits_only) == 12:
            return "+" + digits_only

    # Fallback: if looks like countrycode+number in 10..15 digits, prefix '+'
    if 10 <= len(digits_only) <= 15:
        return "+" + digits_only

    return None


def send_sms(to_phone: str, message: str) -> Optional[str]:
    """Send SMS via Fast2SMS if API key exists; otherwise noop.

    Returns provider message id or None.
    """
    api_key = os.getenv("FAST2SMS_API_KEY")
    if not api_key:
        return None

    # Normalize to E.164; Fast2SMS expects numbers without '+' for India
    normalized = _normalize_phone(to_phone) or ""
    if normalized.startswith('+91'):
        recipients = normalized.replace('+91', '', 1)
    elif normalized.startswith('+'):
        # Non-India: attempt to strip leading '+' only
        recipients = normalized[1:]
    else:
        recipients = normalized
    if not recipients or not recipients.isdigit():
        return None

    payload = {
        "route": "v3",
        "sender_id": os.getenv("FAST2SMS_SENDER_ID", "TXTIND"),
        "message": message,
        "language": "english",
        "flash": 0,
        "numbers": recipients,
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url="https://www.fast2sms.com/dev/bulkV2",
        data=data,
        headers={
            "authorization": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp_data = resp.read()
            try:
                obj = json.loads(resp_data.decode('utf-8'))
                if obj.get('return') is True:
                    return str(obj.get('request_id') or obj.get('message') or 'ok')
            except Exception:
                pass
            return None
    except urllib.error.HTTPError:
        return None
    except urllib.error.URLError:
        return None


def send_whatsapp(to_phone: str, message: str) -> Optional[str]:
    """Send WhatsApp message via Fast2SMS WhatsApp API if credentials exist; otherwise noop.

    Returns provider message id or None.
    """
    api_key = os.getenv("WHATSAPP_API_KEY")
    instance_id = os.getenv("WHATSAPP_INSTANCE_ID")
    token = os.getenv("WHATSAPP_TOKEN")
    
    if not api_key or not instance_id or not token:
        return None

    # Normalize to E.164 format for WhatsApp
    normalized = _normalize_phone(to_phone)
    if not normalized:
        return None

    # Remove the '+' prefix for Fast2SMS WhatsApp API
    recipients = normalized[1:] if normalized.startswith('+') else normalized
    
    payload = {
        "route": "whatsapp",
        "sender_id": "WHATSAPP",
        "message": message,
        "language": "english",
        "flash": 0,
        "numbers": recipients,
        "instance_id": instance_id,
        "token": token,
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url="https://www.fast2sms.com/dev/bulkV2",
        data=data,
        headers={
            "authorization": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp_data = resp.read()
            try:
                obj = json.loads(resp_data.decode('utf-8'))
                if obj.get('return') is True:
                    return str(obj.get('request_id') or obj.get('message') or 'ok')
            except Exception:
                pass
            return None
    except urllib.error.HTTPError:
        return None
    except urllib.error.URLError:
        return None


def send_message(to_phone: str, message: str, message_type: str = "sms") -> Optional[str]:
    """Send message via SMS or WhatsApp based on message_type.
    
    Args:
        to_phone: Phone number to send message to
        message: Message content
        message_type: "sms" or "whatsapp"
    
    Returns:
        Provider message id or None
    """
    if message_type.lower() == "whatsapp":
        return send_whatsapp(to_phone, message)
    else:
        return send_sms(to_phone, message)


