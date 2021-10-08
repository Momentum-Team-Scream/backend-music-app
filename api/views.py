from django.http import request
from django.shortcuts import get_object_or_404, render
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes

from .permissions import IsInstructorAndLessonOwner
from .models import PracticeLog, User, Lesson, Note
from .serializers import NoteSerializer, PracticeLogSerializer, StudentLessonSerializer, StudentProfileSerializer, UserSerializer, LessonSerializer, ListLessonsSerializer, ProfileSerializer

class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.user.is_instructor == True:
            serializer_class = StudentProfileSerializer
        return serializer_class

class SharedProfileViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


class LessonViewSet(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_instructor == True:
            queryset = Lesson.objects.filter(author=self.request.user, lesson_date=date.today())
        if self.request.user.is_instructor == False:
            queryset = Lesson.objects.filter(student=self.request.user).order_by('-lesson_date', '-lesson_time')
        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'GET':
            serializer_class = ListLessonsSerializer
        if self.request.method == 'POST':
            serializer_class = LessonSerializer
        if self.request.user.is_instructor == False:
            serializer_class = StudentLessonSerializer
        return serializer_class
        
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def put(self, request, pk, format=None):
        lesson = self.get_object(pk)
        serializer = LessonSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        serializer = StudentProfileSerializer(student, context={'request': request})
        output["students"].append(serializer.data)
    return JsonResponse(output)
    
class PracticeLogViewSet(ModelViewSet):
    queryset = PracticeLog.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PracticeLogSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)