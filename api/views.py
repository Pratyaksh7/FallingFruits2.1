from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import LocationSerializer
from ecommerce.models import Location
# Create your views here.

@api_view(['GET'])
def Overview(request):
    api_urls = {
        'location-list/' : 'For All the Locations',
        'location-detail/id/' : 'For a particular location',
        'location-create/': 'for creating a new location',
        'location-update/id/': 'For updating a location',
        'location-delete/id/': 'For deleting a location'
    }
    return Response(api_urls)

@api_view(['GET'])
def LocationList(request):
    locations = Location.objects.all()
    serializer = LocationSerializer(locations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def LocationDetail(request, pk):
    locations = Location.objects.get(id=pk)
    serializer = LocationSerializer(locations, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def LocationCreate(request):
    serializer = LocationSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def LocationUpdate(request, pk):
    location = Location.objects.get(id=pk)
    serializer = LocationSerializer(instance=location, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def LocationDelete(request, pk):
    location = Location.objects.get(id=pk)
    location.delete()

    return Response("Your location with id {} has been deleted.".format(pk))



