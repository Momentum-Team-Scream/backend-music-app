from rest_framework import serializers
import djoser
from .models import Lesson, Note, PracticeLog, User

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
    created_at = serializers.DateTimeField(format='%b. %d, %Y at %I:%M %p', read_only=True)
    class Meta:
        model = Note
        fields = ('body', 'lesson', 'is_assignment', 'created_at')

class AddLessonSerializer(serializers.ModelSerializer):
    lesson_date = serializers.DateField("%b. %d, %Y")
    lesson_time = serializers.TimeField("%I:%M %p")
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    created_at = serializers.DateTimeField(format='%b. %d, %Y at %I:%M %p', read_only=True)
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField('combined_student_name')
    lesson_date = serializers.DateField("%b. %d, %Y")
    lesson_time = serializers.TimeField("%I:%M %p")
    note = NoteSerializer (many=True, read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    created_at = serializers.DateTimeField(format='%b. %d, %Y at %I:%M %p', read_only=True)

    def combined_student_name (self, obj):
        student = '{} {}'.format(obj.student.first_name, obj.student.last_name) 
        return student

    class Meta:
        model = Lesson
        fields = (
            "pk", 
            "lesson_date", 
            "lesson_time", 
            "plan", 
            "student", 
            "author", 
            "created_at", 
            "note")

class ListLessonsSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField('combined_student_name')
    lesson_date = serializers.SerializerMethodField('combined_lesson_date_time')

    def combined_student_name (self, obj):
        student_name = '{} {}'.format(obj.student.first_name, obj.student.last_name) 
        return student_name
        
    def combined_lesson_date_time (self, obj):
        date = obj.lesson_date
        time = obj.lesson_time
        lesson_date = '{} at {}'.format(date.strftime("%b. %d, %Y"), time.strftime("%I:%M %p"))
        return lesson_date
    class Meta:
        model = Lesson
        fields = ("pk", "student_name", "lesson_date")


class StudentLessonSerializer(serializers.ModelSerializer):
    lesson_date = serializers.SerializerMethodField('combined_lesson_date_time')
    note = NoteSerializer (many=True, read_only=True)
    
    def combined_lesson_date_time (self, obj):
        date = obj.lesson_date
        time = obj.lesson_time
        lesson_date = '{} at {}'.format(date.strftime("%b. %d, %Y"), time.strftime("%I:%M %p"))
        return lesson_date

    class Meta:
        model = Lesson
        fields = ("pk", "lesson_date", "note")
    
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
            "emergency_contact_name",
            "emergency_contact_phone")

class PracticeLogSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%b. %d, %Y at %I:%M %p', read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model = PracticeLog
        fields = ("pk", "time_practiced", "body", "created_at", "author")
