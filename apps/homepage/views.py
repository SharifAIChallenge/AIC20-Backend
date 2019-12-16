from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.homepage.models import Homepage
from apps.homepage.serializers import HomePageSerializer


@api_view(['GET'])
def get_homepage(request):
    homepage = Homepage.objects.get(id=1)
    serializer = HomePageSerializer(homepage)
    return Response(serializer.data, status=status.HTTP_200_OK)
