from django.apps import AppConfig


class MakeupBackendConfig(AppConfig):
    name = "makeup_backend"
def ready(self):
    import makeup_backend.signals