from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags

def send_password_reset_email(email, token):
    """
    Sends a password reset email to the user.
    """
    subject = "Password Reset Request"
    # The token is sent in the email body for the user to copy
    html_message = f'<p>Your password reset token is: <strong>{token}</strong></p>'
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [email],
        html_message=html_message
    )