from collections import OrderedDict
from rest_framework.reverse import reverse
from rest_framework import serializers
from lesson.models import CourseModel, UnitModel, WordModel
from my_user.models import UserStudyWordModel, UserStudySessionModel
from my_user.serializers import UserStudySessionSerializer
from api.config import Config


class CourseSerializer(serializers.ModelSerializer):
    units_count = serializers.SerializerMethodField()
    words_count = serializers.SerializerMethodField()

    def get_units_count(self, obj: CourseModel):
        count = UnitModel.objects.filter(course=obj).count()
        return count

    def get_words_count(self, obj: CourseModel):
        count = WordModel.objects.filter(unit__course=obj).count()
        return count

    class Meta:
        model = CourseModel
        fields = "__all__"


class UnitSerializer(serializers.ModelSerializer):
    words_count = serializers.SerializerMethodField()

    def get_words_count(self, obj: UnitModel):
        count = WordModel.objects.filter(unit=obj).count()
        return count

    def validate(self, data):

        course = data["course"]
        units_order = UnitModel.objects.filter(course=course).values_list(
            "order", flat=True
        )
        max_order = max(units_order, default=0)
        order = data.get("order", 0)
        if order in units_order:
            raise serializers.ValidationError("Order already exists")
        if order == 0:
            order = max_order + 1
        # if no order then get the last order
        # if order then check if not duplicate
        return super().validate(data)

    # def create(self, validated_data):

    #     if order in units_order:
    #         raise

    #     elif order == 0:
    #         order = max_order

    #     validated_data["order"] = order

    #     return Comment(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get("email", instance.email)
    #     instance.content = validated_data.get("content", instance.content)
    #     instance.created = validated_data.get("created", instance.created)
    #     return instance

    class Meta:
        model = UnitModel
        fields = "__all__"


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordModel
        fields = "__all__"


class LearningReadSerializer(serializers.Serializer):
    question = serializers.CharField(
        max_length=1024,
        allow_blank=True,
    )
    next_url = serializers.CharField(max_length=1024, allow_blank=True)
    study_type = serializers.ChoiceField(choices=UserStudyWordModel.STUDY_TYPE_CHOICES)

    answer = WordSerializer(many=False, required=False)
    words = WordSerializer(many=True, required=False)
    metadata = UserStudySessionSerializer(many=False, required=False)

    def to_internal_value(self, data: dict):
        answer_instance = data.pop("answer")  # type: WordModel
        words_instance = data.pop("words")
        user_study_session = data.pop("metadata")  # type: UserStudySessionModel

        request = self.context.get("request")
        url_learn_id = self.context["learn_id"]
        pk = self.context["pk"]
        next_url = ""
        if (
            url_learn_id < user_study_session.max_session
            and url_learn_id < user_study_session.max_correct
        ):
            next_url = reverse(
                "lesson:UnitViewSet-start-learning",
                kwargs={"pk": pk, "learn_id": url_learn_id + 1},
                request=request,
            )
            next_url = str(next_url)
            # change the url to https if the api is not local
            if not Config.API.IS_LOCAL:
                next_url = str(next_url).replace("http", "https")
        data["next_url"] = next_url

        values = super().to_internal_value(data)

        values["answer"] = WordSerializer(
            instance=answer_instance, context={"request": request}
        ).data
        # if just only one word instance, then serialize it as a single object
        if isinstance(words_instance, WordModel):
            values["words"] = [
                WordSerializer(
                    instance=words_instance, many=False, context={"request": request}
                ).data
            ]
        else:
            values["words"] = WordSerializer(
                instance=words_instance, many=True, context={"request": request}
            ).data
        values["metadata"] = UserStudySessionSerializer(
            instance=user_study_session, context={"request": request}
        ).data
        return values

    def to_representation(self, instance: OrderedDict):
        answer = instance.pop("answer")
        words = instance.pop("words")
        metadata = instance.pop("metadata")
        data = super().to_representation(instance)
        data["answer"] = answer
        data["words"] = words
        data["metadata"] = metadata
        return data
