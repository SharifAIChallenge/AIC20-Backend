from django.utils import timezone

from ..models import Challenge, Tournament, TournamentTypes


class TournamentCreator:

    def __init__(self, challenge, end_time, tournament_type=TournamentTypes.HOURLY):
        self.challenge = challenge
        self.end_time = end_time
        self.tournament_type = tournament_type
        self.tournament = ''
        pass

    def __call__(self):
        pass

    def _create_tournament(self):
        self.tournament = Tournament.objects.create(challenge=self.challenge, type=self.tournament_type,
                                                    end_time=self.end_time)

    def _create_stages(self):
        pass
