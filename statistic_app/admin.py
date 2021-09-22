from django.contrib import admin

# Register your models here.
# для регистрации админки
from .models import UserStatistic, UserLocation, Profile, Project, AgentProject, HistoryProject

admin.site.register(UserLocation)
admin.site.register(Profile)
admin.site.register(UserStatistic)
admin.site.register(Project)
admin.site.register(AgentProject)
admin.site.register(HistoryProject)