from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    USER_CREATE_PASSWORD_RETYPE = True
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone', 'is_instructor', 'emergency_contact_name', 'emergency_contact_phone']

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True) 
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_phone =  models.CharField(validators=[phone_regex], max_length=17) 
    instructor = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='students')
    is_instructor = models.BooleanField(default=True)

    def __repr__(self):
        return f"<User username={self.username}>"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tag(models.Model):
    tag = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tag
    
    
class Lesson(models.Model):
    lesson_date = models.DateField(auto_now_add=False, auto_now=False)
    lesson_time = models.TimeField(auto_now_add=False, auto_now=False)
    plan = models.TextField(blank=True, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        ordering = ['lesson_date', 'lesson_time']

    def __str__(self):
        return f"{self.lesson_date} {self.student}"


class Note(models.Model):
    body = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="note")
    is_assignment = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.body}"


class PracticeLog(models.Model):
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='practice')
    time_practiced = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True,)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.body}"

class Document(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    upload = models.FileField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents', blank=True, null=True)
    students = models.ManyToManyField(User, blank=True, related_name='document_students')
    tags = models.ManyToManyField(Tag, blank=True, related_name='document_tags')