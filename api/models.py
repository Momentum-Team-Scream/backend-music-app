from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Note(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    lesson = models.ForeignKey(
        to="Lesson", on_delete=models.CASCADE, related_name="lesson_note")
    is_shared = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.title}"