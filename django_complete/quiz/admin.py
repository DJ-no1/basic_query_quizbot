from django.contrib import admin
from .models import Quiz, QuizQuestion, QuizSession, QuizAnswer, QuizStatistics


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['topic', 'difficulty', 'total_questions', 'created_at']
    list_filter = ['difficulty', 'created_at']
    search_fields = ['topic', 'session_id']
    readonly_fields = ['session_id', 'created_at', 'updated_at']


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 0
    fields = ['order', 'question', 'correct_answer', 'difficulty']
    readonly_fields = ['order']


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question_preview', 'correct_answer', 'difficulty', 'order']
    list_filter = ['difficulty', 'quiz__difficulty']
    search_fields = ['question', 'quiz__topic']
    
    def question_preview(self, obj):
        return obj.question[:50] + "..." if len(obj.question) > 50 else obj.question
    question_preview.short_description = "Question"


@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'current_score', 'current_question_index', 'is_completed', 'started_at']
    list_filter = ['is_completed', 'started_at']
    readonly_fields = ['started_at', 'last_activity']


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['session', 'question_preview', 'selected_option', 'is_correct', 'answered_at']
    list_filter = ['is_correct', 'answered_at']
    
    def question_preview(self, obj):
        return obj.question.question[:30] + "..." if len(obj.question.question) > 30 else obj.question.question
    question_preview.short_description = "Question"


@admin.register(QuizStatistics)
class QuizStatisticsAdmin(admin.ModelAdmin):
    list_display = ['session', 'total_questions_answered', 'correct_answers', 'percentage']
    readonly_fields = ['total_questions_answered', 'correct_answers', 'incorrect_answers', 'percentage']
