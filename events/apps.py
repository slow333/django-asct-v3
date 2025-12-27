from django.apps import AppConfig

class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'
    
    def ready(self):
        try:
            import reportlab.rl_config
            reportlab.rl_config.warnOnMissingFontGlyphs = 0
        except ImportError:
            pass
