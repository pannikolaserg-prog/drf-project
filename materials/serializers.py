from rest_framework import serializers

from users.models import Subscription
from .models import Course, Lesson
from users.validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[validate_youtube_url])
    description = serializers.CharField(validators=[validate_youtube_url])

    count_lesson_with_same_description = serializers.SerializerMethodField()

    def get_count_lesson_with_same_description(self, lesson):
        return Lesson.objects.filter(description=lesson.description).count()

    class Meta:
        model = Lesson
        fields = (
            "__all__"
        )
        read_only_fields = ("owner", "created_at", "updated_at")

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.IntegerField(source="lessons.count", read_only=True)

    class Meta:
        model = Course
        fields = ["id", "name", "description", "created_at", "lessons", "lessons_count"]
        read_only_fields = ["id", "created_at"]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

class CourseDetailSerializers(serializers.ModelSerializer):
    course_with_same_description = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["name", "description", "course_with_same_description"]

    def get_course_with_same_description(self, course):
        return list(Course.objects.filter(description=course.description).values('id', 'name'))


