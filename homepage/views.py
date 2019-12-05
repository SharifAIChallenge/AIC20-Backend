from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def get_homepage(request):
    return Response(status=status.HTTP_200_OK)
