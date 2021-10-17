from django.db import models
from django.db.models.deletion import CASCADE
from rest_framework import serializers
from .models import Document, Lesson, Note, PracticeLog, Tag, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name", 
            "last_name", 
            "username",
            "email", 
            "phone", 
            "emergency_contact_name", 
            'emergency_contact_phone')


class NoteSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%b. %d, %Y at %-I:%M%p', read_only=True)
    class Meta:
        model = Note
        fields = ('pk', 'body', 'lesson', 'is_assignment', 'created_at')


class AddLessonSerializer(serializers.ModelSerializer):
    lesson_date = serializers.DateField("%b. %d, %Y")
    lesson_time = serializers.TimeField("%-I:%M%p")
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    created_at = serializers.DateTimeField(format='%b. %d, %Y at %-I:%M%p', read_only=True)
    class Meta:
        model = Lesson
        fields = '__all__'


class PreviousLessonSerializer(serializers.ModelSerializer):
    lesson_date = serializers.DateField(format='%b. %d, %Y')
    lesson_time = serializers.TimeField(format='%-I:%M%p')
    note = NoteSerializer (many=True, read_only=True)
    class Meta:
        model = Lesson
        fields = ("pk", 'student', "lesson_date", "lesson_time", "plan", "note")


class LessonSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField('combined_student_name')
    lesson_date = serializers.DateField("%b. %d, %Y")
    lesson_time = serializers.TimeField("%-I:%M%p")
    note = NoteSerializer (many=True, read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    created_at = serializers.DateTimeField(format='%b. %d, %Y at %-I:%M%p', read_only=True)

    def combined_student_name (self, obj):
        student_name = '{} {}'.format(obj.student.first_name, obj.student.last_name) 
        return student_name

    class Meta:
        model = Lesson
        fields = (
            "pk", 
            "lesson_date", 
            "lesson_time", 
            "plan", 
            "student",
            "student_name",
            "author", 
            "created_at", 
            "note")


class ListLessonsSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField('combined_student_name')
    # lesson_date = serializers.SerializerMethodField('combined_lesson_date_time')
    lesson_date = serializers.DateField(format='%b. %d, %Y')
    lesson_time = serializers.TimeField(format='%-I:%M%p')

    def combined_student_name (self, obj):
        student_name = '{} {}'.format(obj.student.first_name, obj.student.last_name) 
        return student_name
    class Meta:
        model = Lesson
        fields = ("pk", "student", "student_name", "lesson_date", 'lesson_time')


class StudentLessonSerializer(serializers.ModelSerializer):
    lesson_date = serializers.DateField(format='%b. %d, %Y')
    lesson_time = serializers.TimeField(format='%-I:%M%p')
    note = NoteSerializer (many=True, read_only=True)
    class Meta:
        model = Lesson
        fields = ("pk", 'student', "lesson_date", "lesson_time", "plan", "note")


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk", 
            "first_name", 
            "last_name", 
            "username", 
            "email",
            "phone", 
            "instructor",
            "emergency_contact_name",
            "emergency_contact_phone",
            )


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "first_name", "last_name", "username", "email")


class PracticeLogSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%b. %d, %Y at %-I:%M%p', read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model = PracticeLog
        fields = ("pk", "time_practiced", "body", "created_at", "author")


class DocumentSerializer(serializers.ModelSerializer):
    uploaded_at = serializers.DateTimeField(format='%b. %d, %Y at %-I:%M%p', read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    tags = serializers.SlugRelatedField(slug_field='slug', many=True, read_only=True)
    students = serializers.SlugRelatedField(slug_field='username', many=True, read_only=True)
    class Meta:
        model = Document
        fields = ('pk', 'uploaded_at', 'title', 'upload', 'author', 'students', 'tags')


class StudentSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "is_instructor",
            "instructor",
            "first_name", 
            "last_name", 
            "username",
            "email", 
            "phone", 
            "emergency_contact_name", 
            "emergency_contact_phone"
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("pk", "slug", "created_by")