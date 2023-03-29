from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import *
from .serializers import *

# City
# list all cities


@api_view(['GET'])
def getCities(request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data)


# add city
@api_view(['POST'])
def addCity(request):
    serializer = CitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

##############################################################
# Terrains
# list all terrains


@api_view(['GET'])
def getTerrains(request):
    Terrains = Terrain.objects.all()
    serializer = TerrainSerializer(Terrains, many=True)
    return Response(serializer.data)


# add terrain
@api_view(['POST'])
def addTerrain(request):
    serializer = TerrainSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# delete terrain
@api_view(['DELETE'])
def deleteTerrain(request, terrain_id):
    try:
        terrain = Terrain.objects.get(pk=terrain_id)
    except Terrain.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    terrain.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# update terrain
@api_view(['PUT'])
def updateTerrain(request, pk):
    try:
        terrain = Terrain.objects.get(pk=pk)
    except Terrain.DoesNotExist:
        return Response(status=404)

    serializer = TerrainSerializer(terrain, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

##################################################################

# type
# list all types


@api_view(['GET'])
def getTypes(request):
    types = Type.objects.all()
    serializer = TypeSerializer(types, many=True)
    return Response(serializer.data)


# add type
@api_view(['POST'])
def addType(request):
    serializer = TypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# delete type
@api_view(['DELETE'])
def deleteType(request, type_id):
    try:
        type = Type.objects.get(pk=type_id)
    except Type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    type.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# update type
@api_view(['PUT'])
def updateType(request, pk):
    try:
        type = Type.objects.get(pk=pk)
    except Type.DoesNotExist:
        return Response(status=404)

    serializer = TypeSerializer(type, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)
