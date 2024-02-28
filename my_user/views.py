from rest_framework import viewsets
from my_user.models import UserStudyWordModel
from my_user.serializers import UserStudyWordSerializer


class UserStudyWordViewSet(viewsets.ModelViewSet):
    queryset = UserStudyWordModel.objects.all()
    serializer_class = UserStudyWordSerializer
