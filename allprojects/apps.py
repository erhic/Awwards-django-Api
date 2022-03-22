from django.apps import AppConfig


class AllprojectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'allprojects'
    
    def ready(self):
        import allprojects.signals

