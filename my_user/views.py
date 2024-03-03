from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from my_user.models import UserStudyWordModel
from my_user.serializers import UserStudyWordSerializer


class UserStudyWordViewSet(viewsets.ModelViewSet):
    queryset = UserStudyWordModel.objects.all()
    serializer_class = UserStudyWordSerializer

    @action(detail=True, methods=["get"])
    def correct(self, request, pk=None):
        user_study_word = self.get_object()  # type: UserStudyWordModel
        user_study_word.right_count += 1
        user_study_word.save()
        serializer = self.get_serializer(user_study_word)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def wrong(self, request, pk=None):
        user_study_word = self.get_object()  # type: UserStudyWordModel
        user_study_word.wrong_count += 1
        user_study_word.save()
        serializer = self.get_serializer(user_study_word)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
