from django.contrib import admin

from reservations.models import Reservation, Player, Field, TypeField

admin.site.register(Reservation)
admin.site.register(Field)
admin.site.register(Player)
admin.site.register(TypeField)
# Register your models here.
