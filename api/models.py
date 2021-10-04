from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Lesson(models.Model):
    title = models.CharField(max_length=250)
    lesson_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)