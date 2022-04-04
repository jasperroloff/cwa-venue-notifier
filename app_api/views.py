# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_api.serializers import LocationSerializer


@api_view(['POST'])
def create_location(request):
    if request.method == 'GET':
        serializer = LocationSerializer(data=request.data)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'POST':
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
