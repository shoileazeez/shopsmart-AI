from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.utils.email import send_password_reset_email
from authentication.models import PasswordResetToken

@receiver(post_save, sender=PasswordResetToken)
def password_reset_token_created_handler(sender, instance, created, **kwargs):
    """
    Handler that sends email when PasswordResetToken is created
    """
    if created:
        send_password_reset_email(instance.user.email, instance.code)