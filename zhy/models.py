from django.db import models


# Create your models here.
class Student(models.Model):
    student_no = models.CharField(max_length=32, unique=True)
    student_name = models.CharField(max_length=32)
    student_gender = models.CharField(max_length=32,default="")
    student_birth = models.CharField(max_length=32,default="")
    student_sdept = models.CharField(max_length=32,default="")
    student_age=models.IntegerField(null=True)


class C(models.Model):
    cno=models.CharField(max_length=32,unique =True)
    cname = models.CharField(max_length=32)
    credit= models.IntegerField()

class SC(models.Model):
    student_no = models.CharField(max_length=32)
    cno = models.CharField(max_length=32)
    mark = models.IntegerField()
