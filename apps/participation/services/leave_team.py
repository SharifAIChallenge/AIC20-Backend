from apps.participation.models import Team, Participant


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

    def _leave_team(self):
        self.request.user.participant.team = None
        self.request.user.participant.save()
