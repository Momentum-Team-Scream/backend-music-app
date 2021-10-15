from django.http import request
from django.shortcuts import get_object_or_404, render

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.postgres.search import SearchVector

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from datetime import date, datetime
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import action, api_view, permission_classes

from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.response import Response

from .permissions import IsInstructorAndLessonOwner, IsInstructorOfStudent, IsStudentOwner, IsStudentofInstructor
from .models import Document, PracticeLog, Tag, User, Lesson, Note
from .serializers import AddLessonSerializer, DocumentSerializer, NoteSerializer, PracticeLogSerializer, StudentLessonSerializer, StudentProfileSerializer, StudentSignupSerializer, StudioSerializer, TagSerializer, UserSerializer, LessonSerializer, ListLessonsSerializer, ProfileSerializer, StudentSignupSerializer

class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if not self.request.user.is_instructor:
            serializer_class = StudentProfileSerializer
        return serializer_class


class SharedProfileViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]


class LessonViewSet(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = AddLessonSerializer
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
            serializer_class = AddLessonSerializer
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


# #Lists student lessons for instructor to view
class StudentLessonsListViewSet(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = StudentLessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Lesson.objects.filter(student=self.kwargs['student_pk']).order_by('-lesson_date', '-lesson_time')
        return queryset

class PreviousLessonViewSet(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lesson = get_object_or_404(Lesson, pk=self.kwargs['pk']) 
        queryset = Lesson.objects.filter(student=self.kwargs['student_pk']).order_by('-lesson_date', '-lesson_time').exclude(lesson_date__gt=lesson.lesson_date)[:5]
        return queryset


class LessonDetailViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def list_students(request):
#     if not (request.user.is_authenticated and request.user.is_instructor):
#         return HttpResponse(status=403) 
#     students = request.user.students.all()
#     output = {}
#     output["instructor"] = UserSerializer(request.user).data
#     output["students"] = []
#     for student in students:
#         serializer = StudentProfileSerializer(student, context={'request': request})
#         output["students"].append(serializer.data)
#     return JsonResponse(output)

class StudioViewSet (ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsInstructorOfStudent]
    serializer_class = StudioSerializer

    def get_queryset(self):
        queryset = self.request.user.students.all()
        if self.request.query_params.get("search"):
            search_term = self.request.query_params.get("search")
            queryset = self.request.user.students.all().annotate(search=SearchVector('first_name', 'last_name', 'username')).filter(search__icontains=search_term)
            return queryset
        return queryset


class PracticeLogViewSet(ModelViewSet):
    queryset = PracticeLog.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PracticeLogSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class DocumentCreateView(ModelViewSet):
    queryset = Document.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class StudentSignupViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = StudentSignupSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer): 
        is_instructor = False
        instructor = User.objects.get(pk=self.kwargs['pk'])
        username = serializer.validated_data["username"]
        serializer.save(is_instructor=is_instructor, instructor=instructor)
        user = User.objects.get(username = username)
        user.set_password(self.request.data["password"])
        user.save()

class FileUploadView(RetrieveUpdateAPIView):
    parser_class = (FileUploadParser,)

    def put(self, request, pk, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        f = request.data['file']
        document = get_object_or_404(Document, pk=pk)
        document.upload.save(f.name, f, save=True)
        return Response(status=status.HTTP_201_CREATED)
    
    
class DocumentDetailViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        document = get_object_or_404(Document, pk=self.kwargs.get('pk'))
        title = document.title
        tags = document.tags
        students = document.students.add()
        kwargs['partial'] = True
        return self.update(request, title, tags, students, *args, **kwargs,)
    
    
class TagView(ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer
