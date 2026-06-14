from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer, CourseDetailSerializers


class CourseViewSet(ModelViewSet):
    """ViewSet для работы с курсами"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializers
        return CourseSerializer


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """API для списка уроков и создания нового"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API для получения, обновления и удаления урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
