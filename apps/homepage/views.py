from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from apps.accounts.models import Profile
from apps.challenge.models import Game, Submission
from apps.participation.models import Team
from apps.staff.models import Staff
from apps.staff.serializers import StaffSerializer
from .models import Intro, TimelineEvent, Prize, Stat, Sponsor, WhyThisEvent, Quote
from .serializers import IntroSerializer, TimelineEventSerializer, PrizeSerializer, StatSerializer, \
    SponsorSerializer, WhyThisEventSerializer, QuoteSerializer


class HomepageView(GenericAPIView):

    def get(self, request):
        data = {
            'intro': IntroSerializer(Intro.objects.last()).data,
            'timeline': TimelineEventSerializer(TimelineEvent.objects.all().order_by('id').order_by('order'),
                                                many=True).data,
            'prizes': PrizeSerializer(Prize.objects.all().order_by('id'), many=True).data,
            'stats': StatSerializer(Stat.objects.all(), many=True).data,
            'sponsors': SponsorSerializer(Sponsor.objects.all(), many=True).data,
            'why': WhyThisEventSerializer(WhyThisEvent.objects.all(), many=True).data,
            'quotes': QuoteSerializer(Quote.objects.all(), many=True).data,

            'teams': Team.objects.count(),
            'registers': Profile.objects.count(),
            'staffs': StaffSerializer(Staff.objects.all().order_by('?')[:5], many=True).data,
            'games': Game.objects.count(),
            'submissions': Submission.objects.count(),
        }
        return Response(data)


class TermsOfUseView(GenericAPIView):

    def get(self, request):
        data = {
            'term': Intro.objects.first().term_of_use
        }
        return Response(data)
