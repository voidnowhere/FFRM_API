from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


@api_view(['GET'])
def getReservation(request):
    reservation = Reservations.objects.all()
    serializers = ReservationSerializer(reservation, many=True)
    return Response(serializers.data)

@api_view(['POST'])
def addResrvation(request):
    serializers = ReservationSerializer(data=request.data)
    if serializers.is_valid():
        serializers.save()
    return Response(serializers.data)

@api_view(['DELETE'])
def cancelReservation(request, pk):
    try:
        reservation = Reservations.objects.get(pk=pk)
    except Reservations.DoesNotExist:
        return Response({"error": "reservation Does Not Exist"},status=status.HTTP_404_NOT_FOUND)
    if reservation.isPaid:
        return Response({"error": "Cannot cancel paid reservation"}, status=status.HTTP_400_BAD_REQUEST)
    reservation.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)