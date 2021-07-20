from django.contrib import admin

# Register your models here.
# для регистрации админки
from .models import UserStatistic, UserLocation, Profile

admin.site.register(UserLocation)
admin.site.register(Profile)
admin.site.register(UserStatistic)
