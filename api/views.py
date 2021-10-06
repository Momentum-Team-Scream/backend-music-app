from django.shortcuts import get_object_or_404, render
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

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
            queryset = Lesson.objects.filter(author=self.request.user)
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
        
class ProfileViewSet(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentProfileSerializer
    
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.user.is_instructor == True:
            serializer_class = ProfileSerializer
        return serializer_class

class LessonDetailViewSet(RetrieveUpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = ListLessonsSerializer
    permission_classes = [IsAuthenticated]
    
    # def get_serializer_class(self):
    #     serializer_class = self.serializer_class
    #     if self.request.method == 'PUT':
    #         serializer_class = LessonSerializer
    #     return serializer_class

class AddNoteViewSet(ListCreateAPIView):
    queryset = Note.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer


    def perform_create(self, serializer):
        serializer.save()

