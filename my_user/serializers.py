from rest_framework import serializers
from my_user.models import UserStudyWordModel


class UserStudyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStudyWordModel
        fields = "__all__"
