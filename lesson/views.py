from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotAcceptable
from drf_spectacular.utils import extend_schema
from my_user.models import UserStudyWordModel, UserStudySessionModel
from my_user.serializers import (
    UserStudyWordPostSerializer,
)
from lesson.models import CourseModel, UnitModel, WordModel
from lesson.serializers import (
    CourseSerializer,
    UnitSerializer,
    WordSerializer,
    LearningReadSerializer,
)


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

    @action(
        detail=True,
        methods=["GET", "POST"],
    )
    def finish(self, request, pk, *args, **kwargs):
        print("pk", pk)
        return Response("ok", status=status.HTTP_200_OK)

    @extend_schema(
        description="learn a word of the unit",
        responses={200: LearningReadSerializer()},
    )
    @action(
        detail=True,
        url_path=r"start-learning/(?P<learn_id>[^/.]+)",
        # url_path=r"start_learning/(?P<learn_id>\d+)",
        url_name="start-learning",
        methods=["GET", "POST"],
    )
    def start_learning(self, request, pk, learn_id, *args, **kwargs):
        test = request.query_params.get("test", False)
        test = bool(test)

        user = request.user
        learn_id = int(learn_id)
        unit = self.get_object()

        user_study_session, user_study_session_created = (
            UserStudySessionModel.objects.get_or_create(user=user)
        )
        if request.method == "GET":
            all_course_units = UnitModel.objects.filter(course=unit.course)

            words = list(WordModel.objects.filter(unit=unit)[0:4])
            # words = WordModel.objects.filter(unit=unit).order_by("?")[0:4]
            correct_word = words[0]
            user_study_session.words.add(correct_word)

            user_word_study, user_word_study_created = (
                UserStudyWordModel.objects.get_or_create(user=user, word=correct_word)
            )

            data = {
                "question": "",
                "words": [correct_word],
                "answer": correct_word,
                "next_url": "",
                "study_type": user_word_study.study_type,
                "metadata": user_study_session,
            }

            if user_word_study.study_type == UserStudyWordModel.INTRO:
                data["words"] = correct_word
                data["answer"] = correct_word
            # TODO add more study types listening and writing
            elif user_word_study.study_type == UserStudyWordModel.CARD or True:
                question = f"what is {correct_word.definition}"
                data["question"] = question
                data["words"] = words
                data["answer"] = correct_word
            else:
                raise NotAcceptable("Invalid study type")

            user_study_session.save()
            learning_read_serializer = LearningReadSerializer(
                data=data, context={"request": request, "learn_id": learn_id, "pk": pk}
            )
            learning_read_serializer.is_valid(raise_exception=True)
            return Response(learning_read_serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            serializer = UserStudyWordPostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            word = get_object_or_404(WordModel, pk=serializer.validated_data["id"])
            headers = self.get_success_headers(serializer.data)
            user_study_session = get_object_or_404(
                UserStudySessionModel, user=user, learn_id=learn_id
            )
            user_word_study, user_word_study_created = (
                UserStudyWordModel.objects.get_or_create(user=user, word=word)
            )
            last_word = user_study_session.words.last()
            user_study_session.learn_id += 1
            if last_word == word:
                user_word_study.next_step()
                user_study_session.correct += 1
            else:
                user_word_study.previous_step()
                user_study_session.incorrect += 1

            user_study_session.save()

            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )


class WordViewSet(viewsets.ModelViewSet):
    queryset = WordModel.objects.all()
    serializer_class = WordSerializer
