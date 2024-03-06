from rest_framework import serializers
from lesson.models import LessonModel, UnitModel, WordModel


class LessonSerializer(serializers.ModelSerializer):
    units_count = serializers.SerializerMethodField()
    words_count = serializers.SerializerMethodField()

    def get_units_count(self, obj: LessonModel):
        count = UnitModel.objects.filter(lesson=obj).count()
        return count

    def get_words_count(self, obj: LessonModel):
        count = WordModel.objects.filter(unit__lesson=obj).count()
        return count

    class Meta:
        model = LessonModel
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
