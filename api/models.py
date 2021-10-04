from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_CREATE_PASSWORD_RETYPE = True
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'emergency_contact_name', 'emergency_contact_phone']

    def __repr__(self):
        return f"<User username={self.username}>"

    def __str__(self):
        return self.username


class Note(models.Model):
    body = models.TextField()
    lesson = models.ForeignKey(
        to="Lesson", on_delete=models.CASCADE, related_name="lesson_note")
    is_assignment = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.title}"


class Lesson(models.Model):
    lesson_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
