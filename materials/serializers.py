from rest_framework import serializers

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    count_lesson_with_same_description = serializers.SerializerMethodField()

    def get_count_lesson_with_same_description(self, lesson):
        return Lesson.objects.filter(description=lesson.description) .count()

    class Meta:
        model = Lesson
        fields = ('id',
                  'name', ''
                  'description',
                  'preview',
                  'video_url',
                  'course',
                  'owner',
                  'created_at',
                  'updated_at',
                  'count_lesson_with_same_description')

class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов с выводом уроков"""
    # Поле для вывода всех уроков курса (связь через related_name='lessons')
    lessons = LessonSerializer(many=True, read_only=True)

    # Поле для вывода количества уроков
    lessons_count = serializers.IntegerField(source='lessons.count', read_only=True)

    # Альтернативный вариант через SerializerMethodField
    # lessons_count = serializers.SerializerMethodField()

    # def get_lessons_count(self, obj):
    #     return obj.lessons.count()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'created_at', 'lessons', 'lessons_count']
        read_only_fields = ['id', 'created_at']


class CourseDetailSerializers(serializers.ModelSerializer):
    course_with_same_description = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("name", "description", "course_with_same_description")

    def get_course_with_same_description(self, course):
        return Course.objects.filter(description=course.description)
