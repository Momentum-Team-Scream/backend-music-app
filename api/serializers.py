from rest_framework import serializers
from .models import Lesson, User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email")


class LessonSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(read_only=True, slug_field="username")
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")
    lesson_date = serializers.DateTimeField(format='%b. %d at %I:%M %p', read_only=True)
    class Meta:
        model = Lesson
        fields = ("lesson_date", "student", "author", "created_at")

class ListLessonsSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(read_only=True, slug_field="last_name")
    lesson_date = serializers.DateTimeField(format='%b. %d at %I:%M %p', read_only=True)
    class Meta:
        model = Lesson
        fields = ("student", "lesson_date")