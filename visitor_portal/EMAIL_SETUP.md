# Email Setup for Visitor Management System

This system now uses **email** for sending OTP verification codes and visitor notifications, instead of SMS/WhatsApp.

## Configuration Steps

### 1. Create Gmail App Password (for Gmail accounts)

1. Go to your Google Account settings: https://myaccount.google.com/
2. Navigate to **Security** → **2-Step Verification** (enable it if not already enabled)
3. Scroll down to **App passwords**
4. Select **App**: "Mail" and **Device**: "Other (Custom name)"
5. Enter "Visitor Management System" and click **Generate**
6. Copy the 16-character password

### 2. Set up Environment Variables

Create or update the `.env` file in the project root (`visitor_management/.env`) with the following:

```env
# Email Configuration
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password_here
DEFAULT_FROM_EMAIL=your.email@gmail.com
```

### 3. Using a Different Email Provider

If you're not using Gmail, update these settings in `visitor_portal/visitor_portal/settings.py`:

**For Outlook/Office365:**
```python
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
```

**For Yahoo:**
```python
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 587
```

**For Custom SMTP:**
```python
EMAIL_HOST = 'smtp.yourprovider.com'
EMAIL_PORT = 587  # or 465 for SSL
EMAIL_USE_TLS = True  # Use False if using SSL on port 465
```

## How It Works

1. **Visitor Registration**: When a visitor enters their email and clicks "Send OTP", a 6-digit verification code is sent to their email address.

2. **Employee Notifications**: When a visitor arrives, the system automatically sends an email notification to the employee they are visiting.

## Testing Email Functionality

### Test in Development

By default, the system uses SMTP backend. For testing without sending actual emails, you can temporarily change `EMAIL_BACKEND` in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

This will print emails to the console instead of sending them.

### Test with Actual Emails

1. Set up your email credentials in `.env` file
2. Run the Django server: `python manage.py runserver`
3. Navigate to the visitor intake page
4. Enter a visitor's email and click "Send OTP"
5. Check the email inbox for the verification code

## Troubleshooting

**Email not being sent:**
- Check that `.env` file exists and contains correct credentials
- Verify app password is correct (Gmail) or password is correct (other providers)
- Check spam/junk folder
- Enable "Less secure app access" if using non-Google accounts (not recommended for Gmail)

**SMTP Authentication Error:**
- Ensure you're using an app password, not your regular password
- Check that 2FA is enabled (for Gmail)
- Verify email and password are correct

**Connection Timeout:**
- Check your firewall settings
- Ensure port 587 is open (or use port 465 with SSL)
- Try different network

## No Additional Setup Required

Unlike SMS/WhatsApp which required:
- ❌ API keys and credentials
- ❌ Document verification for WhatsApp
- ❌ Phone number validation
- ❌ Third-party service integration

Email only requires:
- ✅ Standard email credentials
- ✅ SMTP server access
- ✅ Works immediately with proper credentials

