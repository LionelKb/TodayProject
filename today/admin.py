from django.contrib import admin
from .models import Event, EventType, City

admin.site.register(EventType)
admin.site.register(City)
admin.site.register(Event)