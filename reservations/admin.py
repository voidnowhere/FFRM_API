from django.contrib import admin

from .models import Reservation, Payment

admin.site.register(Reservation)
admin.site.register(Payment)
