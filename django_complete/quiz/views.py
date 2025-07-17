from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db import transaction
import json
import uuid

from .models import Quiz, QuizQuestion, QuizSession, QuizAnswer, QuizStatistics
from .ai_service import ai_quiz_service


def index(request):
    """Home page for the quiz application"""
    return render(request, 'quiz/index.html')


@require_http_methods(["POST"])
def generate_quiz(request):
    """Generate a new quiz using AI"""
    try:
        # Get form data
        topic = request.POST.get('topic', '').strip()
        difficulty = request.POST.get('difficulty', 'medium')
        num_questions = int(request.POST.get('num_questions', 10))
        
        if not topic:
            messages.error(request, 'Topic is required')
            return redirect('quiz:index')
        
        # Validate inputs
        if difficulty not in ['easy', 'medium', 'hard']:
            difficulty = 'medium'
        
        if num_questions < 1 or num_questions > 20:
            num_questions = 10
        
        # Generate quiz using AI
        quiz_data = ai_quiz_service.generate_quiz(topic, difficulty, num_questions)
        
        # Create quiz in database
        with transaction.atomic():
            # Create the quiz
            quiz = Quiz.objects.create(
                session_id=str(uuid.uuid4()),
                topic=quiz_data.topic,
                difficulty=quiz_data.difficulty,
                total_questions=len(quiz_data.questions)
            )
            
            # Create questions
            for idx, question_data in enumerate(quiz_data.questions):
                QuizQuestion.objects.create(
                    quiz=quiz,
                    question=question_data.question,
                    option_a=question_data.option_a,
                    option_b=question_data.option_b,
                    option_c=question_data.option_c,
                    option_d=question_data.option_d,
                    correct_answer=question_data.correct_answer,
                    explanation=question_data.explanation,
                    difficulty=question_data.difficulty,
                    order=idx
                )
            
            # Create quiz session
            quiz_session = QuizSession.objects.create(quiz=quiz)
            
            # Create statistics
            QuizStatistics.objects.create(session=quiz_session)
        
        # Store quiz session ID in Django session
        request.session['quiz_session_id'] = quiz.session_id
        
        return redirect('quiz:quiz_detail', session_id=quiz.session_id)
        
    except Exception as e:
        messages.error(request, f'Error generating quiz: {str(e)}')
        return redirect('quiz:index')


def quiz_detail(request, session_id):
    """Display quiz questions"""
    try:
        quiz = get_object_or_404(Quiz, session_id=session_id)
        quiz_session = get_object_or_404(QuizSession, quiz=quiz)
        
        # Get current question
        questions = quiz.questions.all()
        current_index = quiz_session.current_question_index
        
        if current_index >= len(questions):
            # Quiz completed, redirect to results
            return redirect('quiz:quiz_results', session_id=session_id)
        
        current_question = questions[current_index]
        
        # Calculate progress
        progress_percentage = ((current_index) / len(questions)) * 100
        
        context = {
            'quiz': quiz,
            'quiz_session': quiz_session,
            'current_question': current_question,
            'question_number': current_index + 1,
            'total_questions': len(questions),
            'progress_percentage': progress_percentage,
            'options': current_question.options,
        }
        
        return render(request, 'quiz/quiz_detail.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading quiz: {str(e)}')
        return redirect('quiz:index')


@require_http_methods(["POST"])
def submit_answer(request, session_id):
    """Submit an answer for a quiz question"""
    try:
        quiz = get_object_or_404(Quiz, session_id=session_id)
        quiz_session = get_object_or_404(QuizSession, quiz=quiz)
        
        # Get submitted answer
        selected_option = request.POST.get('selected_option')
        if selected_option is None:
            messages.error(request, 'Please select an answer')
            return redirect('quiz:quiz_detail', session_id=session_id)
        
        selected_option = int(selected_option)
        
        # Get current question
        questions = quiz.questions.all()
        current_index = quiz_session.current_question_index
        
        if current_index >= len(questions):
            return redirect('quiz:quiz_results', session_id=session_id)
        
        current_question = questions[current_index]
        
        # Check if already answered
        existing_answer = QuizAnswer.objects.filter(
            session=quiz_session, 
            question=current_question
        ).first()
        
        if existing_answer:
            # Already answered, move to next question
            quiz_session.current_question_index += 1
            quiz_session.save()
            return redirect('quiz:quiz_detail', session_id=session_id)
        
        # Calculate score
        is_correct = selected_option == current_question.correct_answer
        score_change = 1 if is_correct else 0
        
        # Save answer
        QuizAnswer.objects.create(
            session=quiz_session,
            question=current_question,
            selected_option=selected_option,
            is_correct=is_correct,
            score_change=score_change
        )
        
        # Update session
        quiz_session.current_score += score_change
        quiz_session.current_question_index += 1
        
        # Check if quiz is completed
        if quiz_session.current_question_index >= len(questions):
            quiz_session.is_completed = True
        
        quiz_session.save()
        
        # Update statistics
        stats = quiz_session.statistics
        stats.update_statistics()
        
        return redirect('quiz:quiz_detail', session_id=session_id)
        
    except Exception as e:
        messages.error(request, f'Error submitting answer: {str(e)}')
        return redirect('quiz:quiz_detail', session_id=session_id)


def quiz_results(request, session_id):
    """Display quiz results"""
    try:
        quiz = get_object_or_404(Quiz, session_id=session_id)
        quiz_session = get_object_or_404(QuizSession, quiz=quiz)
        
        if not quiz_session.is_completed:
            return redirect('quiz:quiz_detail', session_id=session_id)
        
        # Get all answers with questions
        answers = quiz_session.answers.select_related('question').order_by('question__order')
        
        # Get statistics
        stats = quiz_session.statistics
        
        # Prepare detailed results
        detailed_results = []
        for answer in answers:
            question = answer.question
            detailed_results.append({
                'question': question.question,
                'options': question.options,
                'selected_option': answer.selected_option,
                'correct_answer': question.correct_answer,
                'is_correct': answer.is_correct,
                'explanation': question.explanation,
                'selected_text': question.options[answer.selected_option],
                'correct_text': question.options[question.correct_answer],
            })
        
        context = {
            'quiz': quiz,
            'quiz_session': quiz_session,
            'stats': stats,
            'detailed_results': detailed_results,
        }
        
        return render(request, 'quiz/results.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading results: {str(e)}')
        return redirect('quiz:index')


def restart_quiz(request, session_id):
    """Restart the quiz from the beginning"""
    try:
        quiz = get_object_or_404(Quiz, session_id=session_id)
        quiz_session = get_object_or_404(QuizSession, quiz=quiz)
        
        # Reset session data
        quiz_session.current_score = 0
        quiz_session.current_question_index = 0
        quiz_session.is_completed = False
        quiz_session.save()
        
        # Delete existing answers
        quiz_session.answers.all().delete()
        
        # Reset statistics
        stats = quiz_session.statistics
        stats.total_questions_answered = 0
        stats.correct_answers = 0
        stats.incorrect_answers = 0
        stats.percentage = 0.0
        stats.save()
        
        messages.success(request, 'Quiz restarted successfully!')
        return redirect('quiz:quiz_detail', session_id=session_id)
        
    except Exception as e:
        messages.error(request, f'Error restarting quiz: {str(e)}')
        return redirect('quiz:index')


@require_http_methods(["GET"])
def quiz_status(request, session_id):
    """API endpoint to get quiz status (JSON response)"""
    try:
        quiz = get_object_or_404(Quiz, session_id=session_id)
        quiz_session = get_object_or_404(QuizSession, quiz=quiz)
        stats = quiz_session.statistics
        
        data = {
            'quiz_id': session_id,
            'topic': quiz.topic,
            'difficulty': quiz.difficulty,
            'total_questions': quiz.total_questions,
            'current_question_index': quiz_session.current_question_index,
            'current_score': quiz_session.current_score,
            'is_completed': quiz_session.is_completed,
            'statistics': {
                'total_answered': stats.total_questions_answered,
                'correct': stats.correct_answers,
                'incorrect': stats.incorrect_answers,
                'percentage': stats.percentage,
            }
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
