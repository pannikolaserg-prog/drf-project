from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CourseViewSet, LessonListCreateAPIView,
                    LessonRetrieveUpdateDestroyAPIView)

router = SimpleRouter()
router.register("courses", CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListCreateAPIView.as_view(), name="lesson_list_create"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDestroyAPIView.as_view(),
        name="lesson_detail",
    ),
]
