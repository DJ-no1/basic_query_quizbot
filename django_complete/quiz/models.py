from django.db import models
from django.contrib.sessions.models import Session
import uuid
import json


class DifficultyChoice(models.TextChoices):
    EASY = 'easy', 'Easy'
    MEDIUM = 'medium', 'Medium'
    HARD = 'hard', 'Hard'


class Quiz(models.Model):
    """Django model for Quiz"""
    session_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    topic = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=10, choices=DifficultyChoice.choices, default=DifficultyChoice.MEDIUM)
    total_questions = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Quiz: {self.topic} ({self.total_questions} questions)"


class QuizQuestion(models.Model):
    """Django model for Quiz Questions"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.IntegerField()  # 0-3 for options A-D
    explanation = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DifficultyChoice.choices)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    @property
    def options(self):
        """Return options as a list"""
        return [self.option_a, self.option_b, self.option_c, self.option_d]
    
    def __str__(self):
        return f"Q{self.order + 1}: {self.question[:50]}..."


class QuizSession(models.Model):
    """Django model for Quiz Sessions and Scoring"""
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE, related_name='session')
    current_score = models.IntegerField(default=0)
    current_question_index = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Session for {self.quiz.topic} - Score: {self.current_score}"


class QuizAnswer(models.Model):
    """Django model for storing user answers"""
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_option = models.IntegerField()  # 0-3 for options A-D
    is_correct = models.BooleanField()
    score_change = models.IntegerField()
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['session', 'question']
    
    def __str__(self):
        return f"Answer to Q{self.question.order + 1} - {'Correct' if self.is_correct else 'Incorrect'}"


class QuizStatistics(models.Model):
    """Django model for quiz statistics"""
    session = models.OneToOneField(QuizSession, on_delete=models.CASCADE, related_name='statistics')
    total_questions_answered = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    
    def update_statistics(self):
        """Update statistics based on answers"""
        answers = self.session.answers.all()
        self.total_questions_answered = answers.count()
        self.correct_answers = answers.filter(is_correct=True).count()
        self.incorrect_answers = answers.filter(is_correct=False).count()
        
        if self.total_questions_answered > 0:
            self.percentage = (self.correct_answers / self.total_questions_answered) * 100
        else:
            self.percentage = 0.0
        
        self.save()
    
    def __str__(self):
        return f"Stats for {self.session.quiz.topic} - {self.percentage:.1f}%"
