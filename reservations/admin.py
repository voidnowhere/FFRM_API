from django.contrib import admin

from reservations.models import Reservations, Players, Field

admin.site.register(Reservations)
admin.site.register(Field)
admin.site.register(Players)
# Register your models here.
