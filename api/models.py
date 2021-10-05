from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_CREATE_PASSWORD_RETYPE = True
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    emergency_contact_name = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    emergency_contact_phone =  models.CharField(validators=[phone_regex], max_length=17) 
    
    is_instructor = models.BooleanField(default=False)

    def __repr__(self):
        return f"<User username={self.username}>"

    def __str__(self):
        return self.username


class Lesson(models.Model):
    lesson_date = models.DateTimeField(auto_now_add=False, auto_now=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        ordering = ['-lesson_date']

    def __str__(self):
        return f"{self.lesson_date}"


class Note(models.Model):
    body = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="note")
    is_assignment = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.body}"



