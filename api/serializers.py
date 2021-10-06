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
    student = serializers.SlugRelatedField(read_only=True, slug_field="username")
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")
    note = NoteSerializer (many=True, read_only=True)
    created_at = serializers.DateTimeField(format='%b. %d, %Y at %I:%M %p', read_only=True)
    class Meta:
        model = Lesson
        fields = ("lesson_date", "student", "author", "created_at", "note")

class ListLessonsSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField('combined_student_name')

    def combined_student_name (self, obj):
        student_name = '{} {}'.format(obj.student.first_name, obj.student.last_name) 
        return student_name
    class Meta:
        model = Lesson
        fields = ("student_name", "lesson_date")
        
class StudioSerializer(serializers.ModelSerializer):
    students = UserSerializer(many=True, read_only=True)
    studio_instructor = UserSerializer(many=False, read_only=True)
    class Meta:
        model = User
        fields = ("is_instructor", "instructor")
        
    def create_studio(self, validated_data):
        User = self.model 
        studio = User.objects.all()
        if User.instructor(validated_data) == True:
            User = self.studio_instructor
        else:
            User = self.students     
            
        return studio(**validated_data)