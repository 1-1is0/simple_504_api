from django.contrib import admin
from lesson.models import CourseModel, UnitModel, WordModel

# Register your models here.

admin.site.register(CourseModel)
admin.site.register(UnitModel)
admin.site.register(WordModel)
