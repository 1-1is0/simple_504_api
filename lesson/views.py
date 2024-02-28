from rest_framework import viewsets
from lesson.models import CourseModel, UnitModel, WordModel
from lesson.serializers import CourseSerializer, UnitSerializer, WordSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = CourseModel.objects.all()
    serializer_class = CourseSerializer


class UnitViewSet(viewsets.ModelViewSet):
    queryset = UnitModel.objects.all()
    serializer_class = UnitSerializer


class WordViewSet(viewsets.ModelViewSet):
    queryset = WordModel.objects.all()
    serializer_class = WordSerializer
