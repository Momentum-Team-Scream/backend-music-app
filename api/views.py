from django.http import request
from django.shortcuts import get_object_or_404, render
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from datetime import date
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes

from .permissions import IsInstructorAndLessonOwner
from .models import User, Lesson, Note
from .serializers import NoteSerializer, StudentProfileSerializer, UserSerializer, LessonSerializer, ListLessonsSerializer, ProfileSerializer

class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.user.is_instructor == True:
            serializer_class = StudentProfileSerializer
        return serializer_class

class LessonViewSet(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # breakpoint()
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_instructor == True:
            queryset = Lesson.objects.filter(author=self.request.user, lesson_date=date.today())
        if self.request.user.is_instructor == False:
            queryset = Lesson.objects.filter(student=self.request.user)
        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'GET':
            serializer_class = ListLessonsSerializer
        return serializer_class
        
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LessonDetailViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsInstructorAndLessonOwner]

class ProfileViewSet(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentProfileSerializer
    
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.user.is_instructor == True:
            serializer_class = ProfileSerializer
        return serializer_class

class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer


    def perform_create(self, serializer):
        serializer.save()

# Listing Instructor Studio
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_students(request):
    if not (request.user.is_authenticated and request.user.is_instructor):
        return HttpResponse(status=403) 
    students = request.user.students.all()
    output = {}
    output["instructor"] = UserSerializer(request.user).data
    output["students"] = []
    for student in students:
        serializer = StudentProfileSerializer(student)
        output["students"].append(serializer.data)
    return JsonResponse(output)
    
