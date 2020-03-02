from django.apps import AppConfig


class ChallengeConfig(AppConfig):
    name = 'challenge'

    def ready(self):
        import apps.challenge.signals