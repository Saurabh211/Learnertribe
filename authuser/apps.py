from django.apps import AppConfig


class AuthuserConfig(AppConfig):
    name = 'authuser'

    def ready(self):
        import authuser.signals