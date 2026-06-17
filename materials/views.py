from django.contrib.auth import get_permission_codename
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsModer
from .models import Course, Lesson
from .serializers import (CourseDetailSerializers, CourseSerializer,
                          LessonSerializer)


class CourseViewSet(ModelViewSet):
    """ViewSet для работы с курсами"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializers
        return CourseSerializer

    def get_permissions(self):
        if self.action == ["create", "destroy"]:
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer,)
        return super().get_permissions()

class LessonListCreateAPIView(generics.ListCreateAPIView):
    """API для списка уроков и создания нового"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API для получения, обновления и удаления урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
