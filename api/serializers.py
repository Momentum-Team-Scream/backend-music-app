from rest_framework import serializers
from .models import Lesson, Note, User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email")

class InstructorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "emergency_contact_name", "emergency_contact_phone")

class LessonSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(read_only=True, slug_field="username")
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")
    lesson_date = serializers.DateTimeField(format='%b. %d at %I:%M %p')
    class Meta:
        model = Lesson
        fields = ("lesson_date", "student", "author", "created_at")

class ListLessonsSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(read_only=True, slug_field="last_name")
    lesson_date = serializers.DateTimeField(format='%b. %d at %I:%M %p')
    class Meta:
        model = Lesson
        fields = ("student", "lesson_date")

class InstructorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ()
        
class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        
class StudentProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "emergency_contact_name", "emergency_contact_phone")

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('body', 'lesson', 'is_assignment', 'created_at')
