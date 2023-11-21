from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message, Profile, Attendance, Tournament, TeachingHours, ServiceHours, PracticalScore

admin.site.register(Profile)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Attendance)
admin.site.register(Tournament)
admin.site.register(TeachingHours)
admin.site.register(ServiceHours)
admin.site.register(PracticalScore)