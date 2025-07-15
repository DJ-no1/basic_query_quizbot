from typing import Dict, List
from backend.models import Quiz, QuizQuestion, AnswerResponse, ScoreResponse
import uuid
from datetime import datetime


class ScoreManager:
    def __init__(self):
        """Initialize the score manager"""
        self.user_sessions: Dict[str, Dict] = {}
        self.scoring_rules = {
            "correct_easy": 1,
            "correct_medium": 2,
            "correct_hard": 3,
            "incorrect_easy": -1,
            "incorrect_medium": -2,
            "incorrect_hard": -3
        }
    
    def create_session(self, quiz: Quiz) -> str:
        """
        Create a new user session for a quiz
        
        Args:
            quiz: The quiz object
            
        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        self.user_sessions[session_id] = {
            "quiz": quiz,
            "score": 0,
            "answers": [],
            "correct_count": 0,
            "incorrect_count": 0,
            "started_at": datetime.now(),
            "last_activity": datetime.now()
        }
        return session_id
    
    def submit_answer(self, session_id: str, question_index: int, selected_option: int) -> AnswerResponse:
        """
        Submit an answer for a question and update score
        
        Args:
            session_id: The user session ID
            question_index: Index of the question being answered
            selected_option: Index of the selected option (0-3)
            
        Returns:
            AnswerResponse with result and score change
        """
        if session_id not in self.user_sessions:
            raise ValueError("Invalid session ID")
        
        session = self.user_sessions[session_id]
        quiz = session["quiz"]
        
        if question_index < 0 or question_index >= len(quiz.questions):
            raise ValueError("Invalid question index")
        
        question = quiz.questions[question_index]
        is_correct = selected_option == question.correct_answer
        
        # Calculate score change
        difficulty = question.difficulty.value
        if is_correct:
            score_change = self.scoring_rules[f"correct_{difficulty}"]
            session["correct_count"] += 1
        else:
            score_change = self.scoring_rules[f"incorrect_{difficulty}"]
            session["incorrect_count"] += 1
        
        # Update session
        session["score"] += score_change
        session["answers"].append({
            "question_index": question_index,
            "selected_option": selected_option,
            "is_correct": is_correct,
            "score_change": score_change,
            "timestamp": datetime.now()
        })
        session["last_activity"] = datetime.now()
        
        return AnswerResponse(
            correct=is_correct,
            correct_answer=question.correct_answer,
            explanation=question.explanation,
            score_change=score_change
        )
    
    def get_score(self, session_id: str) -> ScoreResponse:
        """
        Get the current score for a session
        
        Args:
            session_id: The user session ID
            
        Returns:
            ScoreResponse with current score information
        """
        if session_id not in self.user_sessions:
            raise ValueError("Invalid session ID")
        
        session = self.user_sessions[session_id]
        total_answered = len(session["answers"])
        
        percentage = 0.0
        if total_answered > 0:
            percentage = (session["correct_count"] / total_answered) * 100
        
        return ScoreResponse(
            current_score=session["score"],
            total_questions_answered=total_answered,
            correct_answers=session["correct_count"],
            incorrect_answers=session["incorrect_count"],
            percentage=percentage
        )
    
    def get_session_summary(self, session_id: str) -> Dict:
        """
        Get a complete summary of a user session
        
        Args:
            session_id: The user session ID
            
        Returns:
            Dictionary with session summary
        """
        if session_id not in self.user_sessions:
            raise ValueError("Invalid session ID")
        
        session = self.user_sessions[session_id]
        score_response = self.get_score(session_id)
        
        return {
            "session_id": session_id,
            "quiz_topic": session["quiz"].topic,
            "total_questions": session["quiz"].total_questions,
            "score": score_response.current_score,
            "questions_answered": score_response.total_questions_answered,
            "correct_answers": score_response.correct_answers,
            "incorrect_answers": score_response.incorrect_answers,
            "percentage": score_response.percentage,
            "started_at": session["started_at"],
            "last_activity": session["last_activity"],
            "answers": session["answers"]
        }
    
    def reset_session(self, session_id: str) -> None:
        """
        Reset a user session (clear answers and score)
        
        Args:
            session_id: The user session ID
        """
        if session_id not in self.user_sessions:
            raise ValueError("Invalid session ID")
        
        session = self.user_sessions[session_id]
        session["score"] = 0
        session["answers"] = []
        session["correct_count"] = 0
        session["incorrect_count"] = 0
        session["last_activity"] = datetime.now()
    
    def delete_session(self, session_id: str) -> None:
        """
        Delete a user session
        
        Args:
            session_id: The user session ID
        """
        if session_id in self.user_sessions:
            del self.user_sessions[session_id]
    
    def cleanup_old_sessions(self, max_age_hours: int = 24) -> int:
        """
        Clean up old sessions that haven't been active
        
        Args:
            max_age_hours: Maximum age in hours before cleanup
            
        Returns:
            Number of sessions cleaned up
        """
        current_time = datetime.now()
        sessions_to_delete = []
        
        for session_id, session in self.user_sessions.items():
            age = current_time - session["last_activity"]
            if age.total_seconds() > max_age_hours * 3600:
                sessions_to_delete.append(session_id)
        
        for session_id in sessions_to_delete:
            del self.user_sessions[session_id]
        
        return len(sessions_to_delete)
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """
        Get a leaderboard of top sessions (for demonstration purposes)
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of top sessions sorted by score
        """
        leaderboard = []
        
        for session_id, session in self.user_sessions.items():
            if len(session["answers"]) > 0:  # Only include sessions with answers
                leaderboard.append({
                    "session_id": session_id[:8],  # Shortened for display
                    "topic": session["quiz"].topic,
                    "score": session["score"],
                    "percentage": self.get_score(session_id).percentage,
                    "questions_answered": len(session["answers"])
                })
        
        # Sort by score (descending) then by percentage
        leaderboard.sort(key=lambda x: (-x["score"], -x["percentage"]))
        
        return leaderboard[:limit]
