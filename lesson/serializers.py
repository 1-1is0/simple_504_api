from rest_framework import serializers
from lesson.models import CourseModel, UnitModel, WordModel


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = "__all__"


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitModel
        fields = "__all__"


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordModel
        fields = "__all__"
