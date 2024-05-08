from rest_framework import serializers
from lesson.models import CourseModel, UnitModel, WordModel
from my_user.models import UserStudyWordModel


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

    class Meta:
        model = UnitModel
        fields = "__all__"


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordModel
        fields = "__all__"


class WordStudySerializer(serializers.Serializer):
    word = WordSerializer()
    other_words = WordSerializer(many=True)


class LearningReadSerializer(serializers.Serializer):
    question = serializers.CharField(
        max_length=1024,
        allow_blank=True,
    )
    answer = WordSerializer(many=False, required=False)
    next_url = serializers.CharField(max_length=1024, allow_blank=True)
    study_type = serializers.ChoiceField(choices=UserStudyWordModel.STUDY_TYPE_CHOICES)

    # words = WordSerializer(many=True)
    def to_internal_value(self, data: dict):
        answer_instance = data.pop("answer")
        print("to internal value data", data)
        d = super().to_internal_value(data)
        answer_serializer = WordSerializer(instance=answer_instance)
        d["answer"] = answer_serializer.data
        print("after super", d)
        return d
