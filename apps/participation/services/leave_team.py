from apps.challenge.models import Submission
from apps.participation.models import Team


class LeaveTeam:

    def __init__(self, request, team_name: str):
        self.request = request
        self.team_name = team_name
        self.team = None
        self.valid = True
        self.errors = []

    def __call__(self):
        self._validate_team()
        if self.valid:
            self._validate_user_in_team()
        if self.valid:
            self._check_leave_conditions()
        if self.valid:
            self._leave_team()
        return self.errors

    def _validate_team(self):
        try:
            self.team = Team.objects.get(name=self.team_name)
        except (Team.DoesNotExist, Team.MultipleObjectsReturned) as e:
            self.errors.append(str(e))
            self.valid = False

    def _validate_user_in_team(self):
        for participant in self.team.participants.all():
            if self.request.user.email == participant.user.mail:
                return
        self.valid = False
        self.errors.append("You're Not in this team")

    def _check_leave_conditions(self):
        if self.request.user.participant.team.participants.all().count() != 1 and \
                Submission.objects.filter(user=self.request.user, team=self.request.user.participant.team).exists():
            self.valid = False
            self.errors.append("You can't leave this team, because you have a submission right now")

    def _leave_team(self):
        self.request.user.participant.delete()
        if self.team.participants.all().count() == 0:
            self.team.delete()
