from apps.challenge.models import Submission, ChallengeTypes
from apps.participation.models import Team
from django.utils.translation import ugettext_lazy as _


class LeaveTeam:

    def __init__(self, request):
        self.request = request
        self.team = None
        self.valid = True
        self.errors = []

    def __call__(self):
        if self.valid:
            self._validate_user_in_team()
        if self.valid:
            self._validate_team_challenge_type()
        if self.valid:
            self._check_leave_conditions()
        if self.valid:
            self._leave_team()
        return self.errors

    def _validate_user_in_team(self):
        if hasattr(self.request.user, 'participant') and self.request.user.participant.team:
            self.team = self.request.user.participant.team
            return
        self.valid = False
        self.errors.append(_("You're Not in any team"))

    def _validate_team_challenge_type(self):
        if self.request.user.participant.team.challenge.type == ChallengeTypes.FINAL:
            self.valid = False
            self.errors.append(_("You can't leave your team in final challenge"))

    def _check_leave_conditions(self):
        if Submission.objects.filter(user=self.request.user, team=self.request.user.participant.team).exists():
            self.valid = False
            self.errors.append(_("You can't leave this team, because you have a submission right now"))

    def _leave_team(self):
        self.request.user.participant.delete()
        if self.team.participants.all().count() == 0:
            self.team.delete()
