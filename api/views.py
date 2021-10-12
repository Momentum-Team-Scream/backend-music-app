from django.http import request
from django.shortcuts import get_object_or_404, render

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from datetime import date
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes

from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from .permissions import IsInstructorAndLessonOwner, IsInstructorOfStudent, IsStudentOwner, IsStudentofInstructor
from .models import Document, PracticeLog, User, Lesson, Note
from .serializers import AddLessonSerializer, NoteSerializer, PracticeLogSerializer, StudentLessonSerializer, StudentProfileSerializer, StudentSignupSerializer, UserSerializer, LessonSerializer, ListLessonsSerializer, ProfileSerializer, StudentSignupSerializer

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
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    # def get_permissions(self):
    #     if self.request.user.is_instructor == True:
    #         permission_classes = [IsAuthenticated, IsInstructorOfStudent]
    #     if self.request.user.is_instructor == False:
    #         permission_classes = [IsAuthenticated, IsStudentofInstructor]
    #     return permission_classes


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

class DocumentCreateView(ModelViewSet):
    queryset = Document.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        documents = Document.objects.all()
        context['documents'] = documents
        return context

class StudentSignupViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = StudentSignupSerializer

    def perform_create(self, serializer):         
        serializer.save(is_instructor=False)

        
# class FileUploadView(APIView):
#     parser_class = [FileUploadParser]

#     def put(self, request, format=None):
#         if 'file' not in request.data:
#             raise ParseError("Empty content")
        
#         f = request.data['file']

#         Document.upload.save(f.title, f, save=True)
#         return Response(status=status.HTTP_201_CREATED)
    
#     def delete(self, request, format=None):
#         Document.upload.delete(save=True)
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
class UploadAPIView(UpdateAPIView):


    def update(self, request, *args, **kwargs):
        # The upload_id is obtained from front-end after having successfully uploaded the picture.
        upload_id = request.data['upload_id']
        # Given a variable upload_id containing a 22-character unique file upload ID:
        if upload_id != '' and upload_id != None:
            su = store_upload(
                upload_id, destination_file_path='target_dir/{}.png'.format(upload_id))

        id = self.kwargs.get(self.lookup_url_kwarg)
        your_obj = Document.objects.filter(id=id).get()

        serializer = DocumentSerializer(data=serializer, many=True)
        your_obj.is_valid()
        your_obj.save()
# return Response(serializer.data, status=status.HTTP_201_CREATED)

