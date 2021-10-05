from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Note(models.Model):
    body = models.TextField()
    lesson = models.ForeignKey(
        to="Lesson", on_delete=models.CASCADE, related_name="lesson_note")
    is_assignment = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.body}"


class Lesson(models.Model):
    lesson_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        ordering = ['-lesson_date']

    def __str__(self):
        return f"{self.lesson_date}"
