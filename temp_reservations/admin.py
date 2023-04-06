from django.contrib import admin

from temp_reservations.models import FootBallFieldType, FootBallField, Reservation

admin.site.register(FootBallFieldType)
admin.site.register(FootBallField)
admin.site.register(Reservation)
