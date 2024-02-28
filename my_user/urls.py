from django.urls import path, include
from rest_framework import routers
from my_user.views import UserStudyWordViewSet

app_name = "my_user"

router = routers.DefaultRouter()
router.register(
    r"user_study_word", UserStudyWordViewSet, basename="UserStudyWordViewSet"
)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
]
