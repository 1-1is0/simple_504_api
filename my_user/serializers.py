from rest_framework import serializers
from my_user.models import UserStudyWordModel, UserStudySessionModel


class UserStudyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStudyWordModel
        fields = "__all__"


class UserStudySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStudySessionModel
        fields = "__all__"


class UserStudyWordPostSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
