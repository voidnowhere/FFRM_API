from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.generics import CreateAPIView,UpdateAPIView,DestroyAPIView,RetrieveAPIView,ListAPIView
# City
# list all cities



# list all the zones
class ZoneListAPIView(ListAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

##############################################################
# Fields


# list all fields
class FieldListAPIView(ListAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

# add field
class FieldCreateAPIView(CreateAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

# update field
class FieldUpdateAPIView(UpdateAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

# delete field
class FieldDestroyAPIView(DestroyAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

# retrieve field
class FieldRetrieveAPIView(RetrieveAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
##################################################################

# type
# list all types
class TypeListAPIView(ListAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

# add Type
class TypeCreateAPIView(CreateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

# update Type
class TypeUpdateAPIView(UpdateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

# delete Type
class TypeDestroyAPIView(DestroyAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

# retrieve Type
class TypeRetrieveAPIView(RetrieveAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
##################################################################