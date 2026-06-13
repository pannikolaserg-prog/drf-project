from rest_framework import serializers

from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


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


class CourseDetailSerializers(serializers.ModelSerializer):
    course_with_same_description = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("name", "description", "course_with_same_description")

    def get_course_with_same_description(self, course):
        return Course.objects.filter(description=course.description)
