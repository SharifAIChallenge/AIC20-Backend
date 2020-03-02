from django.apps import AppConfig


class ChallengeConfig(AppConfig):
    name = 'apps.challenge'

    def ready(self):
        import apps.challenge.signals