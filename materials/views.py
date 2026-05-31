from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


# Курс - ViewSet (всё в одном классе)
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# Урок - Generic классы (только 2 класса)
class LessonListCreateAPIView(ListCreateAPIView):
    """GET список уроков, POST создать урок"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """GET один урок, PUT/PATCH обновить, DELETE удалить"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
