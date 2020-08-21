from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.


class UserInfo(AbstractUser):
    NickName = models.CharField(max_length=20, blank=False, null=False)
    phonenumber = models.IntegerField(blank=True,null=True)

class SurveyList(models.Model):
    UUID_S = models.CharField(max_length=40,unique=True)
    username = models.CharField(max_length=40)
    SurveyName = models.CharField(max_length=40)
    SurveyDescription = models.CharField(max_length=300, null=True)
    SurveyType = models.BooleanField(default=False)
    SurveyStatus = models.BooleanField(default=False)
    LastEditTime = models.DateTimeField(auto_now=True)

class QuestionDetail(models.Model):
    UUID_S = models.CharField(max_length=40)
    QTitle = models.CharField(max_length=40)
    QNumber = models.IntegerField()
    QType = models.CharField(max_length=40)
    QDescription = models.TextField(null=True,blank=True)
    QOptions = models.TextField(null=True,blank=True)
    unique_together = (('UUID_S', 'QNumber'),)

class AnswerRecord(models.Model):
    UUID_S = models.CharField(max_length=40)
    username = models.CharField(max_length=40)
    Time = models.DateTimeField(auto_now=True)
    ANum = models.IntegerField()
    AOptions = models.TextField()
