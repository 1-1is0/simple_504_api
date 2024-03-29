from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from lesson.models import LessonModel, UnitModel, WordModel
from lesson.serializers import (
    LessonSerializer,
    UnitSerializer,
    WordSerializer,
    WordStudySerializer,
)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer

    @extend_schema(
        description="Get all units in a lesson",
        responses={200: UnitSerializer(many=True)},
    )
    @action(detail=True, methods=["get"])
    def units(self, request, pk, *args, **kwargs):
        lesson = self.get_object()
        units = UnitModel.objects.filter(lesson=lesson)
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UnitViewSet(viewsets.ModelViewSet):
    queryset = UnitModel.objects.all()
    serializer_class = UnitSerializer

    @extend_schema(
        description="Get all words in a unit",
        responses={200: WordSerializer(many=True)},
    )
    @action(detail=True, methods=["get"])
    def words(self, request, pk, *args, **kwargs):
        unit = self.get_object()
        words = WordModel.objects.filter(unit=unit)
        serializer = WordSerializer(words, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WordViewSet(viewsets.ModelViewSet):
    queryset = WordModel.objects.all()
    serializer_class = WordSerializer

    @extend_schema(
        description="Get all words in a unit",
        responses={200: WordStudySerializer()},
    )
    @action(detail=True, methods=["get"])
    def study(self, request, pk, *args, **kwargs):
        word = self.get_object()
        # get 3 other random words
        other_words = WordModel.objects.exclude(pk=word.pk).order_by("?")[:3]
        serializer = WordStudySerializer(
            {"word": word, "other_words": other_words}, many=False
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
