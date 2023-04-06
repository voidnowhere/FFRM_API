from django.contrib import admin

from reservations.models import Reservation, Player, Field

admin.site.register(Reservation)
admin.site.register(Field)
admin.site.register(Player)
# Register your models here.
