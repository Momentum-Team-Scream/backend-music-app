from django.contrib import admin
from .models import User, Lesson, Note

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['pk',]
    
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'body', 'is_shared', 'created_at',]
