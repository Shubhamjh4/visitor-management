import os
from typing import Optional
from django.core.mail import send_mail
from django.conf import settings


def send_email_notification(to_email: str, subject: str, message: str) -> Optional[str]:
    """Send email notification.
    
    Args:
        to_email: Email address to send to
        subject: Email subject
        message: Email body content
    
    Returns:
        'sent' if successful, None otherwise
    """
    if not to_email or not to_email.strip():
        return None
    
    # In development, if using console backend, it will print to console
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email.strip()],
            fail_silently=False,
        )
        return 'sent'
    except Exception as e:
        # If email fails, log it but don't crash
        print(f"Email sending failed: {e}")
        return None


def send_otp_email(to_email: str, otp_code: str) -> Optional[str]:
    """Send OTP via email.
    
    Args:
        to_email: Visitor email address
        otp_code: 6-digit OTP code
    
    Returns:
        'sent' if successful, None otherwise
    """
    subject = "Your Verification Code"
    message = (
        f"Your verification code is {otp_code}. "
        f"This code will expire in 5 minutes. "
        f"\n\nIf you did not request this code, please ignore this email."
    )
    return send_email_notification(to_email, subject, message)


def send_visitor_notification_email(to_email: str, visitor_name: str, visitor_phone: str, purpose: str) -> Optional[str]:
    """Send email notification to employee about visitor arrival.
    
    Args:
        to_email: Employee email address
        visitor_name: Name of the visitor
        visitor_phone: Phone number of the visitor
        purpose: Purpose of the visit
    
    Returns:
        'sent' if successful, None otherwise
    """
    subject = f"Visitor Alert: {visitor_name} has arrived"
    message = (
        f"{visitor_name} (Phone: {visitor_phone}) has arrived to meet you "
        f"for {purpose}."
        f"\n\nPlease proceed to the reception area to meet your visitor."
    )
    return send_email_notification(to_email, subject, message)

