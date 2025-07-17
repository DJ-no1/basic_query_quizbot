from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('generate/', views.generate_quiz, name='generate_quiz'),
    path('quiz/<str:session_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<str:session_id>/submit/', views.submit_answer, name='submit_answer'),
    path('quiz/<str:session_id>/results/', views.quiz_results, name='quiz_results'),
    path('quiz/<str:session_id>/restart/', views.restart_quiz, name='restart_quiz'),
    
    # API endpoints
    path('api/quiz/<str:session_id>/status/', views.quiz_status, name='quiz_status'),
]
