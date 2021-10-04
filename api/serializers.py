from rest_framework import serializers
from .models import Lesson, User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email")


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("lesson_date", "student", "owner", "created_at")

class ListLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("student", "lesson_date")