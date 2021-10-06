from rest_framework import permissions

class IsInstructorAndLessonOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_instructor == True:
            return True
        if obj.author == request.user:
            return True
        return False