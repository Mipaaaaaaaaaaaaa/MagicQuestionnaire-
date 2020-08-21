from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.UserInfo)
admin.site.register(models.SurveyList)
admin.site.register(models.QuestionDetail)
admin.site.register(models.AnswerRecord)
