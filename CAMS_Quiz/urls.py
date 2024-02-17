from django.urls import path, include
from . import views

urlpatterns = [
  path('/quizset', views.CAMS_QUIZSET, name='quizset'),
  path('/quizquestions/<int:cat_id>', views.CAMS_QUESTIONS, name='quizquestions'),
  path('/submit-answer/<int:cat_id>/<int:quest_id>', views.SUBMIT_ANSWER, name='submit_answer'),
  path('/restart_quiz', views.restart_quiz, name='restart_quiz'),

]