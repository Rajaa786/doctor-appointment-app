from django.contrib import admin

from testApp.models import Appointments, MyUser, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
# admin.site.unregister(User)
admin.site.register(MyUser, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Appointments)
# admin.site.register(AppointmentMade)
