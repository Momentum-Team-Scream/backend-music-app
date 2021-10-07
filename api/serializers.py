from rest_framework import serializers
import djoser
from .models import Lesson, Note, User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email")

class InstructorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "emergency_contact_name", "emergency_contact_phone")

        
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

class LessonSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.filter(is_instructor=False))
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    note = NoteSerializer (many=True, read_only=True)
    created_at = serializers.DateTimeField(format='%b. %d, %Y at %I:%M %p', read_only=True)
    class Meta:
        model = Lesson
        fields = ("lesson_date", "lesson_time", "plan", "student", "author", "created_at", "note")

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
        fields = ("student_name", "lesson_date")

# class LoginSerializer(djoser.serializers.UserSerializer):
#     class Meta:
#         model = User
#         fields = ("token", "is_instructor")