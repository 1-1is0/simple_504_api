from rest_framework import viewsets, status
import random
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from lesson.models import CourseModel, UnitModel, WordModel
from lesson.serializers import (
    CourseSerializer,
    UnitSerializer,
    WordSerializer,
    WordStudySerializer,
)


# todo all views realy only

class CourseViewSet(viewsets.ModelViewSet):
    queryset = CourseModel.objects.all()
    serializer_class = CourseSerializer

    @extend_schema(
        description="Get all units in a course",
        responses={200: UnitSerializer(many=True)},
    )
    @action(detail=True, methods=["get"])
    def units(self, request, pk, *args, **kwargs):
        course = self.get_object()
        units = UnitModel.objects.filter(course=course)
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

    @action(detail=True,
            url_path=r"start-learning/(?P<learn_id>[^/.]+)",
            # url_path=r"start_learning/(?P<learn_id>\d+)",
            url_name="start-learning",
            methods=["get"],
            )
    def start_learning(self, request, pk, learn_id, *args, **kwargs):
        learn_id = int(learn_id)
        unit = self.get_object()
        all_course_units = UnitModel.objects.filter(course=unit.course)
        words = WordModel.objects.filter(unit=unit).order_by("?")[:4]
        currect_word = words[0]
        words_serializer = WordSerializer(words, many=True)
        currect_words_serializer = WordSerializer(currect_word, many=False)

        question = f"what is {currect_word.definition}"
        
        metadata = {
            "max": 15,
            "correct": random.randint(0, 10),
            "incorrect": random.randint(0, 3),
            "currenct": learn_id,
        }


        data = {
            "question": question,
            "words": words_serializer.data,
            "answer": currect_words_serializer.data,
            "metadata": metadata,
            "next": None,
        }

        if learn_id < 15:
            
            # next_learn_url = f"/lesson/unit/{pk}/start_learning/{learn_id}"
            # next_learn_url = reverse(viewname="unitviewset-list", args=[pk, learn_id+1], request=request)
            next_learn_url = reverse("lesson:UnitViewSet-start-learning", kwargs={"pk": pk, "learn_id": learn_id+1}, request=request)
            data["next"] = next_learn_url

        return Response(data, status=status.HTTP_200_OK)

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
