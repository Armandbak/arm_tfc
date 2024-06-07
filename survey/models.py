import datetime
from datetime import date, timedelta


from django.db import models
from django.utils import timezone

from student.models import Student
from teacher.models import Teacher

""" class Question(models.Model):
    text = models.CharField(max_length=255)

class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
"""

from django.db import models
import json
from django.contrib.auth.models import AbstractUser, Permission, Group, User



class Uenseignement(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_debut = models.DateField(blank= True, null= True)
    date_fin = models.DateField(blank= True, null= True)
    uenseignement = models.ForeignKey(Uenseignement, on_delete=models.CASCADE, related_name='uenseignement')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher')
    total_marks = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    text = models.CharField(max_length=255)
    options = models.TextField()
    marks = models.PositiveIntegerField()
    response = models.CharField(max_length=255, blank=True)  # Champ réponse

    def __str__(self):
        return f"{self.course.name} - {self.text}"

    def get_options(self):
        return json.loads(self.options)

    def set_options(self, options_list):
        self.options = json.dumps(options_list)



class Inscription(models.Model):
    cours = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='inscriptions')
    etudiant = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='inscriptions')
    date_inscription = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.etudiant.user.username} inscrit à {self.cours.name} le {self.date_inscription}'

class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    soumis = models.BooleanField(default=False)