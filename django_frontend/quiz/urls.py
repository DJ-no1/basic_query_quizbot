from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz/', views.quiz_page, name='quiz_page'),
    path('api/generate/', views.generate_quiz, name='generate_quiz'),
    path('api/answer/', views.submit_answer, name='submit_answer'),
    path('api/score/', views.get_score, name='get_score'),
    path('api/topics/', views.get_topics, name='get_topics'),
    path('api/reset/', views.reset_quiz, name='reset_quiz'),
]
