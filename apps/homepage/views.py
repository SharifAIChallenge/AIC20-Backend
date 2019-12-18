from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from .models import Intro, TimelineEvent, Prize, Stat
from .serializers import *
from apps.translation.util import translateQuerySet


class HomepageView(GenericAPIView):

    def get(self, request):
        data = {
                'intro': IntroSerializer(Intro.objects.last()).data,
                'timeline': TimelineEventSerializer(TimelineEvent.objects.all(), many=True).data,
                'prizes': PrizeSerializer(Prize.objects.all(), many=True).data,
                'stats': StatSerializer(Stat.objects.all(), many=True).data,
                }
        return Response(data)

