from rest_framework import serializers
from dj_rest_auth.models import TokenModel
from dj_rest_auth.serializers import UserDetailsSerializer


class CustomTokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """

    user = UserDetailsSerializer(read_only=True)

    class Meta:
        model = TokenModel
        fields = ("key", "user")
