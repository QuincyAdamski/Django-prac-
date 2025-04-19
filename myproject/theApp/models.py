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
    students_enrolled = models.IntegerField(default=0)
    #image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    enrolled_users = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)

    def __str__(self):
        return self.title
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    #start_time = models.TimeField(default=datetime.time(9, 0))  # 09:00 AM
    start_time = models.TimeField(default=time(9, 0))
    #end_time = models.TimeField(default=datetime.time(17, 0))   # 05:00 PM
    end_time = models.TimeField(default=time(17, 0))
    location = models.CharField(max_length=200, default="Virtual")
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_users = models.ManyToManyField(User, related_name="registered_events", blank=True)

    def __str__(self):
        return self.title
    
class EventTwo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    
    