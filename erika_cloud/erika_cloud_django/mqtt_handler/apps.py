from django.apps import AppConfig

class MqttHandlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqtt_handler'

    def ready(self):
        import mqtt_handler.handlers
