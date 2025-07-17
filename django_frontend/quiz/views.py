import requests
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import messages


class APIClient:
    """Client to interact with the FastAPI backend"""
    
    def __init__(self):
        self.base_url = settings.BACKEND_API_URL
    
    def get_topics(self):
        try:
            response = requests.get(f"{self.base_url}/quiz/topics")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "suggested_topics": []}
    
    def generate_quiz(self, topic, num_questions=10, difficulty="medium"):
        try:
            data = {
                "topic": topic,
                "num_questions": num_questions,
                "difficulty": difficulty
            }
            response = requests.post(f"{self.base_url}/quiz/generate", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def submit_answer(self, session_id, question_index, selected_option):
        try:
            data = {
                "session_id": session_id,
                "question_index": question_index,
                "selected_option": selected_option
            }
            response = requests.post(f"{self.base_url}/quiz/answer", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def get_score(self, session_id):
        try:
            response = requests.get(f"{self.base_url}/quiz/score/{session_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def reset_quiz(self, session_id):
        try:
            response = requests.post(f"{self.base_url}/quiz/reset/{session_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}


# Initialize API client
api_client = APIClient()


def index(request):
    """Home page with topic selection"""
    topics_data = api_client.get_topics()
    
    context = {
        'suggested_topics': topics_data.get('suggested_topics', []),
        'api_error': topics_data.get('error')
    }
    
    return render(request, 'quiz/index.html', context)


def quiz_page(request):
    """Quiz interface page"""
    # Check if there's quiz data in session
    quiz_data = request.session.get('quiz_data')
    if not quiz_data:
        return redirect('quiz:index')
    
    context = {
        'quiz': quiz_data,
        'session_id': quiz_data.get('session_id')
    }
    
    return render(request, 'quiz/quiz.html', context)


@csrf_exempt
def generate_quiz(request):
    """Generate a new quiz via API"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            topic = data.get('topic', '')
            num_questions = data.get('num_questions', 10)
            difficulty = data.get('difficulty', 'medium')
            
            if not topic:
                return JsonResponse({'error': 'Topic is required'}, status=400)
            
            result = api_client.generate_quiz(topic, num_questions, difficulty)
            
            if 'error' in result:
                return JsonResponse(result, status=500)
            
            # Store quiz data in session
            request.session['quiz_data'] = result
            request.session['current_question'] = 0
            request.session['user_answers'] = []
            
            return JsonResponse({
                'success': True,
                'message': 'Quiz generated successfully',
                'redirect': '/quiz/',
                'session_id': result.get('session_id')
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def submit_answer(request):
    """Submit an answer to a quiz question"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')
            question_index = data.get('question_index')
            selected_option = data.get('selected_option')
            
            if None in [session_id, question_index, selected_option]:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            result = api_client.submit_answer(session_id, question_index, selected_option)
            
            # Update session data
            user_answers = request.session.get('user_answers', [])
            user_answers.append({
                'question_index': question_index,
                'selected_option': selected_option,
                'is_correct': result.get('correct', False)
            })
            request.session['user_answers'] = user_answers
            
            return JsonResponse(result)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_score(request, session_id=None):
    """Get current quiz score"""
    if not session_id:
        session_id = request.GET.get('session_id')
    
    if not session_id:
        return JsonResponse({'error': 'Session ID required'}, status=400)
    
    result = api_client.get_score(session_id)
    return JsonResponse(result)


def get_topics(request):
    """Get suggested topics"""
    result = api_client.get_topics()
    return JsonResponse(result)


@csrf_exempt
def reset_quiz(request):
    """Reset current quiz"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')
            
            if not session_id:
                return JsonResponse({'error': 'Session ID required'}, status=400)
            
            result = api_client.reset_quiz(session_id)
            
            # Clear session data
            request.session.pop('quiz_data', None)
            request.session.pop('current_question', None)
            request.session.pop('user_answers', None)
            
            return JsonResponse(result)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
