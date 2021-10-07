from django.shortcuts import get_object_or_404, render
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from datetime import date

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
        # if self.request.method == 'GET' and self.request.user.is_instructor == False:
        #     serializer_class = ListLessonsSerializer
        if self.request.method == 'POST':
            serializer_class = LessonSerializer
        return serializer_class
        
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
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

