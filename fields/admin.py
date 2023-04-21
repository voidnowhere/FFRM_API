from django.contrib import admin
from .models import Field
from zones.models import Zone

admin.site.register(Zone)
admin.site.register(Field)
