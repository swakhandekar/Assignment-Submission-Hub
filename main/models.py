from django.db import models
from django.contrib.auth.models import User

class Batch(models.Model):
    bname = models.CharField(max_length=2)

    def __str__(self):
        return str(self.bname)

class MyBatch(models.Model):
    batch = models.ForeignKey(Batch)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.user) + str(self.batch)

class Student(models.Model):
    user = models.OneToOneField(User)
    rollno = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.user)

class Teacher(models.Model):
    user = models.OneToOneField(User)
    emp_no = models.CharField(max_length=11,unique=True)

    def __str__(self):
        return str(self.user)

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class Assignment(models.Model):
    title = models.TextField(max_length=100)
    problem_statement  = models.TextField(max_length=1000)
    deadline = models.DateTimeField()
    to_batch = models.ForeignKey(Batch)
    sub = models.ForeignKey(Subject)
    assigned_by = models.ForeignKey(Teacher)

class Submission(models.Model):
    remark = models.CharField(max_length=200,default="")
    scale = models.IntegerField(null=True)
    is_checked = models.BooleanField(default=False)
    is_late = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    assignment = models.ForeignKey(Assignment)