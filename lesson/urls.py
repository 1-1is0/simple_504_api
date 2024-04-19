from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from lesson.views import CourseViewSet, UnitViewSet, WordViewSet

app_name = "lesson"

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"Course", CourseViewSet, basename="Course3ViewSet")
router.register(r"unit", UnitViewSet, basename="UnitViewSet")
router.register(r"word", WordViewSet, basename="WordViewSet")


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
]
