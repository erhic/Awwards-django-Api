from django.contrib import admin

# Register your models here.
from .models import *
#
from .models import Profile
admin.site.register(Profile)
admin.site.register(Account)
admin.site.register(Project)
