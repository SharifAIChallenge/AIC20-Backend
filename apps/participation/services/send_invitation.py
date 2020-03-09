import json
from typing import Union

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from apps.challenge.models import ChallengeTypes
from apps.participation.models import Invitation, Team, InvitationStatusTypes
from apps.participation.serializers import InvitationSerializer


class SendInvitation:

    def __init__(self, request):
        self.request = request
        self.data = json.loads(request.body)
        self.user_email = ''
        self.invitation_serializer = None
        self.user = None
        self.valid = True
        self.errors = []

    def __call__(self):
        self._validate_email()
        if self.valid:
            self._set_user()
        if self.valid:
            self._validate_inviter_has_team()
        if self.valid:
            self._validate_target_has_team()
        if self.valid:
            self._validate_team_filled()
        if self.valid:
            self._validate_team_challenge_type()
        if self.valid:
            self._validate_invited_before()
        if self.valid:
            self._invite()
        return self.invitation_serializer, self.errors

    def _validate_email(self):
        self.user_email = self.data.get('user_email')
        if not self.user_email:
            self.valid = False
            self.errors.append(_("Email Field is required"))

    def _set_user(self):
        try:
            self.user = User.objects.get(email=self.user_email)
        except (User.DoesNotExist, User.MultipleObjectsReturned) as e:
            self.errors.append(str(e))
            self.valid = False

    def _validate_inviter_has_team(self):
        if not hasattr(self.request.user, 'participant'):
            self.valid = False
            self.errors.append(_("You don't have any team to invite other people to it"))

    def _validate_target_has_team(self):
        if hasattr(self.user, 'participant'):
            self.valid = False
            self.errors.append(_('User already has a team'))

    def _validate_team_filled(self):
        if hasattr(self.request.user,
                   'participant') and self.request.user.participant.team.participants.count() >= Team.TEAM_MAX_SIZE:
            self.valid = False
            self.errors.append(_('Your team is full!'))

    def _validate_team_challenge_type(self):
        if hasattr(self.request.user,
                   'participant') and self.request.user.participant.team.challenge.type == ChallengeTypes.FINAL:
            self.valid = False
            self.errors.append((_('You can\'t send invitations in final challenge')))

    def _validate_invited_before(self):
        if Invitation.objects.filter(source=self.request.user, target=self.user,
                                     status=InvitationStatusTypes.NOT_ANSWERED).exists():
            self.valid = False
            self.errors.append(_('Invited before'))

    def _invite(self):
        invitation = Invitation.objects.create(source=self.request.user, target=self.user)
        self.invitation_serializer = InvitationSerializer(invitation)
