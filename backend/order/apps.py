from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order'
    
    def ready(self):
        # Import signal handlers to ensure they're registered when the app is ready.
        try:
            import order.signals.signal  # noqa: F401
        except Exception:
            # Avoid raising during migrations or test discovery if signals import fails.
            pass
