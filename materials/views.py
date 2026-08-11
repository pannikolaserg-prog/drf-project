from django.utils import timezone  # вместо from datetime import timezone
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from users.tasks import notify_subscribers_about_course_update
from users.permissions import IsNotModer, IsOwnerOrModer
from .models import Course, Lesson
from .paginators import CustomPagination
from .serializers import CourseDetailSerializers, CourseSerializer, LessonSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="description from swagger_auto_schema via method_decorator"
))
class CourseViewSet(ModelViewSet):
    """ViewSet для работы с курсами"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializers
        return CourseSerializer

    def get_permissions(self):
        if self.action == 'create':
            # Создание - только не модераторы
            self.permission_classes = [IsAuthenticated, IsNotModer]
        elif self.action == 'destroy':
            # Удаление - только не модераторы
            self.permission_classes = [IsAuthenticated, IsNotModer]
        elif self.action in ['update', 'partial_update']:
            # Обновление - модераторы или владелец
            self.permission_classes = [IsAuthenticated, IsOwnerOrModer]
        elif self.action == 'retrieve':
            # Просмотр - модераторы или владелец
            self.permission_classes = [IsAuthenticated, IsOwnerOrModer]
        else:  # list
            # Список - все авторизованные
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        """Фильтруем курсы в зависимости от роли пользователя"""
        user = self.request.user
        if not user.is_authenticated:
            return Course.objects.none()

        # Модераторы видят все курсы
        if user.groups.filter(name='moderators').exists():
            return Course.objects.all()

        # Обычные пользователи видят только свои курсы
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        """При создании курса автоматически назначаем владельца"""
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course = self.get_object()
        last_updated = course.updated_at  # Сохраняем время ДО обновления

        # Сохраняем курс ВСЕГДА
        serializer.save()

        # Проверяем, прошло ли больше 4 часов (14400 секунд)
        if last_updated:
            time_diff = timezone.now() - last_updated
            if time_diff.total_seconds() < 14400:
                return  # Не отправляем уведомление

        # Отправляем уведомление подписчикам
        notify_subscribers_about_course_update.delay(course.id)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """API для списка уроков и создания нового"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            # Создание - только не модераторы
            self.permission_classes = [IsAuthenticated, IsNotModer]
        else:  # GET
            # Просмотр - все авторизованные
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        """Фильтруем уроки в зависимости от роли пользователя"""
        user = self.request.user
        if not user.is_authenticated:
            return Lesson.objects.none()

        # Модераторы видят все уроки
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()

        # Обычные пользователи видят только свои уроки
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        """При создании урока автоматически назначаем владельца"""
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API для получения, обновления и удаления урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            # Просмотр - модераторы или владелец
            self.permission_classes = [IsAuthenticated, IsOwnerOrModer]
        elif self.request.method in ['PUT', 'PATCH']:
            # Обновление - модераторы или владелец
            self.permission_classes = [IsAuthenticated, IsOwnerOrModer]
        elif self.request.method == 'DELETE':
            # Удаление - только не модераторы
            self.permission_classes = [IsAuthenticated, IsNotModer]
        return super().get_permissions()

    def get_queryset(self):
        """Фильтруем уроки в зависимости от роли пользователя"""
        user = self.request.user
        if not user.is_authenticated:
            return Lesson.objects.none()

        # Модераторы видят все уроки
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()

        # Обычные пользователи видят только свои уроки
        return Lesson.objects.filter(owner=user)
