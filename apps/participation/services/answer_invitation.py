import json

from apps.participation.models import Invitation, InvitationStatusTypes


class AnswerInvitation:

    def __init__(self, request, invitation_id):
        self.request = request
        self.data = json.loads(request.data)
        self.answer = ''
        self.invitation_id = invitation_id
        self.invitation = None
        self.valid = True
        self.errors = []

    def __call__(self):
        self._validate_answer()
        if self.valid:
            self._validate_invitation()
        if self.valid:
            self._answer_invitation()
        return self.errors

    def _validate_answer(self):
        answer = self.data.get('answer')
        if not answer:
            self.valid = False
            self.errors.append("Answer field required")
            return
        if answer == 'accept':
            self.answer = InvitationStatusTypes.ACCEPTED
        elif answer == 'reject':
            self.answer = InvitationStatusTypes.REJECTED
        else:
            self.valid = False
            self.errors.append("Answer Must one of these: accept or reject")

    def _validate_invitation(self):
        try:
            self.invitation = Invitation.objects.get(id=self.invitation_id)
        except (Invitation.DoesNotExist, Invitation.MultipleObjectsReturned) as e:
            self.valid = False
            self.errors.append(str(e))

        if self.invitation.status is not InvitationStatusTypes.NOT_ANSWERED:
            self.valid = False
            self.errors.append('Invitation answered before')

    def _answer_invitation(self):
        self.invitation.status = self.answer
        self.request.user.participant.team = self.invitation.source.participant.team
        self.invitation.save()
        self.request.user.participant.save()
