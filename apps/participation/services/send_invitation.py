import json
from typing import Union

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from apps.participation.models import Invitation
from apps.participation.serializers import InvitationSerializer


class SendInvitation:

    def __init__(self, request):
        self.request = request
        self.data = json.loads(request.data)
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
        if self.request.user.participant.team is None:
            self.valid = False
            self.errors.append(_("You don't have any team to invite other people to it"))

    def _validate_target_has_team(self):
        if self.user.participant.team is not None:
            self.valid = False
            self.errors.append(_('User already has a team'))

    def _invite(self):
        invitation = Invitation.objects.create(source=self.request.user, target=self.user)
        self.invitation_serializer = InvitationSerializer(invitation)
