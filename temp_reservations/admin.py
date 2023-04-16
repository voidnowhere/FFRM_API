from django.contrib import admin

from temp_reservations.models import FieldType, Field, Reservation

admin.site.register(FieldType)
admin.site.register(Field)
admin.site.register(Reservation)
