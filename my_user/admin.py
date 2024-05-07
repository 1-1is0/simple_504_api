from django.contrib import admin
from my_user.models import UserStudyWordModel, UserStudySessionModel

# Register your models here.

admin.site.register(UserStudyWordModel)
admin.site.register(UserStudySessionModel)
