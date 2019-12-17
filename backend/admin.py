from django.contrib import admin
from .models import User, Schedule, Booking, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Schedule)
admin.site.register(Booking)
admin.site.register(Comment)
