from django.contrib import admin
from lesson.models import LessonModel, UnitModel, WordModel

# Register your models here.

admin.site.register(LessonModel)
admin.site.register(UnitModel)
admin.site.register(WordModel)
