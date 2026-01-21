# Email Setup Instructions

## Gmail SMTP Configuration

To send real emails using Gmail, follow these steps:

### Step 1: Enable 2-Step Verification
1. Go to your Google Account: https://myaccount.google.com/
2. Click on **Security** in the left sidebar
3. Under "Signing in to Google", click **2-Step Verification**
4. Follow the prompts to enable 2-Step Verification

### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
   - Or navigate: Google Account → Security → 2-Step Verification → App passwords
2. Select **Mail** as the app
3. Select **Other (Custom name)** as the device
4. Enter "Django" as the custom name
5. Click **Generate**
6. Copy the 16-character password (it will look like: `abcd efgh ijkl mnop`)

### Step 3: Update Django Settings
1. Open `core/core/settings.py`
2. Find the email configuration section (around line 134)
3. Fill in your details:
   ```python
   EMAIL_HOST_USER = 'your-email@gmail.com'  # Your Gmail address
   EMAIL_HOST_PASSWORD = 'abcdefghijklmnop'  # The 16-character App Password (no spaces)
   DEFAULT_FROM_EMAIL = 'your-email@gmail.com'  # Same as EMAIL_HOST_USER
   ```

### Step 4: Test Email
1. Restart your Django server
2. Register a student with a valid email address
3. Check the student's inbox for the confirmation email

## Alternative Email Providers

### Outlook/Hotmail
```python
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@outlook.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'your-email@outlook.com'
```

### Yahoo Mail
```python
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@yahoo.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@yahoo.com'
```

### Custom SMTP Server
```python
EMAIL_HOST = 'smtp.yourdomain.com'
EMAIL_PORT = 587  # or 465 for SSL
EMAIL_USE_TLS = True  # or EMAIL_USE_SSL = True for port 465
EMAIL_HOST_USER = 'your-email@yourdomain.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'your-email@yourdomain.com'
```

## Troubleshooting

### Error: "Authentication failed"
- Make sure you're using an App Password, not your regular Gmail password
- Verify 2-Step Verification is enabled
- Check that EMAIL_HOST_PASSWORD has no spaces

### Error: "Connection refused"
- Check your firewall settings
- Verify EMAIL_HOST and EMAIL_PORT are correct
- Some networks block SMTP ports

### Emails going to spam
- Add SPF and DKIM records to your domain (for custom domains)
- Use a professional email service for production
- Consider using services like SendGrid, Mailgun, or AWS SES

## Security Note

⚠️ **Never commit your email password to Git!**

For production, use environment variables:
```python
import os
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
```

Then set the environment variable on your server.

