from django.contrib import admin

# Register your models here.

from .models import Tanulo, Valasztas, Foglalkozas

admin.site.register(Tanulo)
admin.site.register(Valasztas)
admin.site.register(Foglalkozas)
