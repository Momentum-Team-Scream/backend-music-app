from django.contrib import admin

from .models import PracticeLog, User, Lesson, Note

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'is_instructor']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['pk', 'lesson_date', 'student', 'plan']
    
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'body']

@admin.register(PracticeLog)
class PracticeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'body', 'author', 'created_at']