from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
    
    def ready(self):
        """
        Import signals when Django starts
        This ensures that the signal handlers are registered
        """
        # Avoid circular imports
        import authentication.signals.handlers  # noqa
