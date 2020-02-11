import os

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class InvitationStatusTypes:
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    NOT_ANSWERED = 'not_answered'
    TYPES = (
        (ACCEPTED, 'Invitation Accepted'),
        (REJECTED, 'Invitation Rejected'),
        (NOT_ANSWERED, 'Invitation Not Answered')
    )


class Badge(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField()
    challenge = models.ForeignKey('challenge.Challenge', related_name='badges', on_delete=models.CASCADE)


class Team(models.Model):
    TEAM_MAX_SIZE = 3
    IMAGE_MAX_SIZE = 200 * 1024
    VALID_IMAGE_FORMATS = ('jpeg', 'png', 'jpg')

    name = models.CharField(max_length=100, unique=True)
    badges = models.ManyToManyField('participation.Badge', related_name='teams', null=True, blank=True)
    challenge = models.ForeignKey('challenge.Challenge', related_name='teams', on_delete=models.DO_NOTHING)

    def get_team_image_directory(self, filename):
        return os.path.join(self.name, 'image', filename)

    image = models.ImageField(upload_to=get_team_image_directory, null=True)

    @property
    def is_valid(self):
        return True if self.participants.count() >= 2 else False


class Participant(models.Model):
    user = models.OneToOneField(User, related_name='participant', on_delete=models.CASCADE)
    team = models.ForeignKey('participation.Team', related_name='participants', on_delete=models.CASCADE)


class Invitation(models.Model):
    target = models.ForeignKey(User, related_name='invitations', on_delete=models.CASCADE)
    source = models.ForeignKey(User, related_name='invites', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=InvitationStatusTypes.TYPES,
                              default=InvitationStatusTypes.NOT_ANSWERED)
