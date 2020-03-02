from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Tournament


@receiver(post_save, sender=Tournament)
def create_hourly_tournament(sender, instance: Tournament, created: bool, **kwargs):
    from .services.tournament_creator import TournamentCreator
    from .tasks import run_multi_games

    if created:
        games_ids = TournamentCreator(instance)()
        run_multi_games.delay(games_ids)
