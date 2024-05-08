import random
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotAcceptable, MethodNotAllowed
from drf_spectacular.utils import extend_schema
from my_user.models import UserStudyWordModel, UserStudySessionModel
from my_user.serializers import (
    UserStudyWordSerializer,
    UserStudySessionSerializer,
    UserStudyWordPostSerializer,
)
from lesson.models import CourseModel, UnitModel, WordModel
from lesson.serializers import (
    CourseSerializer,
    UnitSerializer,
    WordSerializer,
    WordStudySerializer,
    LearningReadSerializer,
)
from api.config import Config


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
        print("test", test)

        user = request.user
        learn_id = int(learn_id)
        unit = self.get_object()

        user_study_session, user_study_session_created = (
            UserStudySessionModel.objects.get_or_create(user=user)
        )
        user_study_session_serializer = UserStudySessionSerializer(
            user_study_session, many=False
        )

        if request.method == "GET":
            all_course_units = UnitModel.objects.filter(course=unit.course)

            w = WordModel.objects.filter(unit=unit)[0:4]
            words = list(WordModel.objects.filter(unit=unit)[0:4])
            # words = WordModel.objects.filter(unit=unit).order_by("?")[0:4]
            correct_word = words[0]
            user_study_session.words.add(correct_word)
            words_serializer = WordSerializer(words, many=True)
            correct_word_serializer = WordSerializer(correct_word, many=False)

            user_word_study, user_word_study_created = (
                UserStudyWordModel.objects.get_or_create(user=user, word=correct_word)
            )

            data = {
                "question": "",
                "words": [correct_word_serializer.data],
                "answer": correct_word_serializer.data,
                "next_url": "",
                "study_type": user_word_study.study_type,
            }

            print("word study study type", user_word_study.study_type)
            if user_word_study.study_type == UserStudyWordModel.INTRO:
                data["words"] = [correct_word_serializer.data]
                data["answer"] = correct_word_serializer.data
            elif user_word_study.study_type == UserStudyWordModel.CARD:
                question = f"what is {correct_word.definition}"
                data["question"] = question
                data["words"] = words_serializer.data
                data["answer"] = correct_word_serializer.data
            else:
                raise NotAcceptable("Invalid study type")

            data["metadata"] = user_study_session_serializer.data

            if learn_id < user_study_session.max_session:

                # next_learn_url = f"/lesson/unit/{pk}/start_learning/{learn_id}"
                # next_learn_url = reverse(viewname="unitviewset-list", args=[pk, learn_id+1], request=request)
                next_learn_url = reverse(
                    "lesson:UnitViewSet-start-learning",
                    kwargs={"pk": pk, "learn_id": learn_id + 1},
                    request=request,
                )

                # change the url to https if the api is not local
                if Config.API.IS_LOCAL:
                    data["next_url"] = str(next_learn_url)
                else:
                    data["next_url"] = str(next_learn_url).replace("http", "https")
            else:
                data["next_url"] = ""

            user_study_session.save()
            # TODO add question types

            if test:
                # correct_word_serializer.is_valid(raise_exception=True)
                s_data = {
                    "question": data["question"],
                    # "words": w,
                    "answer": correct_word,
                    "next_url": data["next_url"],
                    "study_type": data["study_type"],
                }
                learning_read_serializer = LearningReadSerializer(
                    data=s_data, context={"request": request}
                )
                print("##### SERIALIZER")
                learning_read_serializer.is_valid(raise_exception=True)
                print("response data", learning_read_serializer.data)
                return Response(
                    learning_read_serializer.data, status=status.HTTP_200_OK
                )
            else:
                return Response(data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            serializer = UserStudyWordPostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            word = get_object_or_404(WordModel, pk=serializer.validated_data["id"])
            headers = self.get_success_headers(serializer.data)
            user_study_session = get_object_or_404(
                UserStudySessionModel, user=user, learn_id=learn_id
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
