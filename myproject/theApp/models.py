import datetime
from datetime import date, time, datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Feature(models.Model):#example model
    name = models.CharField(max_length=100)
    deatails = models.CharField(max_length=500)

class Course(models.Model):
    title = models.CharField(max_length=255)
    instructor = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    students_enrolled = models.IntegerField(default=0)
    #image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    enrolled_users = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)

    def __str__(self):
        return self.title
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200, default="Virtual")
    registered_users = models.ManyToManyField(User, related_name="registered_events", blank=True)

    def __str__(self):
        return self.title
    
    