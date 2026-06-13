from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.viewsets import ModelViewSet

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer, CourseDetailSerializers


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializers
        return CourseSerializer


class LessonListCreateAPIView(ListCreateAPIView):
    """GET список уроков, POST создать урок"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """GET один урок, PUT/PATCH обновить, DELETE удалить"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
