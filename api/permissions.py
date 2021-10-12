from rest_framework import permissions

class IsInstructorAndLessonOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_instructor == True:
            return True
        if obj.author == request.user:
            return True
        return False

# Beginning of permissions class to limit a student profile to only be visible by their instructor.
class IsInstructorOfStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        breakpoint()
        if request.user.is_superuser:
            return True
        if request.user.is_instructor == True:
            return True
        if obj.author == request.user:
            return True
        if obj.instructor == request.user:
            return True
        return False


class IsStudentofInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.students in obj.author.students.all():
            return True
        return False

class IsStudentOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.is_instructor == False:
            return True
        if obj.author == request.user:
            return True
        return False