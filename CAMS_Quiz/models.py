from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class QuizSet(models.Model):
    title=models.CharField(max_length=100)
    time_detail = models.CharField(max_length=100)
    time_limit=models.IntegerField(default=0)

    class Meta:
        verbose_name_plural='Quiz Sets'

    def __str__(self):
        return self.title
    
class QuizQuestion(models.Model):
    category=models.ForeignKey(QuizSet, on_delete=models.CASCADE)
    question=models.TextField()
    opt_1=models.CharField(max_length=500)
    opt_2=models.CharField(max_length=500)
    opt_3=models.CharField(max_length=500)
    opt_4=models.CharField(max_length=500)
    
    
    right_opt=models.CharField(max_length=500)


    class Meta:
        verbose_name_plural='Questions'

    def __str__(self):
        return self.question

class UserSubmittedAnswer(models.Model):
    question=models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    right_answer=models.CharField(max_length=200,blank=True, null=True)

    class Meta:
        verbose_name_plural='User Submitted Answers'