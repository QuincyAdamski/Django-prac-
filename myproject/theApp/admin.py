from django.contrib import admin
from .models import Feature, Course, Event, EventTwo

# Register your models here.
admin.site.register(Feature)
admin.site.register(Course)
admin.site.register(Event)
admin.site.register(EventTwo)
