from django.contrib import admin

from .models import User, Lesson, Note

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['pk', 'lesson_date', 'student',]
    
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'body', 'is_shared',]