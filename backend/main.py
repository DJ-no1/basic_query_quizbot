from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.models import (
    QuizRequest, QuizResponse, AnswerRequest, AnswerResponse, 
    ScoreResponse, DifficultyLevel
)
from backend.quiz_generator import QuizGenerator
from backend.score_manager import ScoreManager
from typing import Dict, List
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Quiz Bot API",
    description="A smart quiz bot that generates quizzes on any topic using LangChain and Google's Generative AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
quiz_generator = None
score_manager = ScoreManager()

@app.on_event("startup")
async def startup_event():
    """Initialize the quiz generator on startup"""
    global quiz_generator
    try:
        quiz_generator = QuizGenerator()
        logger.info("Quiz generator initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize quiz generator: {e}")
        quiz_generator = None

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Quiz Bot API",
        "version": "1.0.0",
        "endpoints": {
            "generate_quiz": "/quiz/generate",
            "submit_answer": "/quiz/answer",
            "get_score": "/quiz/score/{session_id}",
            "get_session": "/quiz/session/{session_id}",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "quiz_generator_available": quiz_generator is not None
    }

@app.post("/quiz/generate", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    """
    Generate a new quiz on the given topic
    
    Args:
        request: QuizRequest with topic, number of questions, and difficulty
        
    Returns:
        QuizResponse with generated quiz or error message
    """
    if quiz_generator is None:
        raise HTTPException(
            status_code=503, 
            detail="Quiz generator is not available. Please check the API configuration."
        )
    
    try:
        logger.info(f"Generating quiz for topic: {request.topic}")
        
        # Generate the quiz
        quiz = quiz_generator.generate_quiz(
            topic=request.topic,
            num_questions=request.num_questions,
            difficulty=request.difficulty
        )
        
        # Validate the quiz
        errors = quiz_generator.validate_quiz(quiz)
        if errors:
            logger.warning(f"Quiz validation errors: {errors}")
            return QuizResponse(
                success=False,
                error=f"Quiz validation failed: {'; '.join(errors)}"
            )
        
        # Create a session for this quiz
        session_id = score_manager.create_session(quiz)
        
        # Add session_id to the response
        response_data = QuizResponse(success=True, quiz=quiz)
        
        # Add session_id to the response (we'll modify the response model if needed)
        logger.info(f"Quiz generated successfully. Session ID: {session_id}")
        
        return JSONResponse(content={
            "success": True,
            "quiz": quiz.dict(),
            "session_id": session_id
        })
        
    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz: {str(e)}")

@app.post("/quiz/answer", response_model=AnswerResponse)
async def submit_answer(request: AnswerRequest, session_id: str):
    """
    Submit an answer for a quiz question
    
    Args:
        request: AnswerRequest with question index and selected option
        session_id: User session ID
        
    Returns:
        AnswerResponse with result and score change
    """
    try:
        logger.info(f"Submitting answer for session {session_id}")
        
        answer_response = score_manager.submit_answer(
            session_id=session_id,
            question_index=request.question_index,
            selected_option=request.selected_option
        )
        
        return answer_response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error submitting answer: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to submit answer: {str(e)}")

@app.get("/quiz/score/{session_id}", response_model=ScoreResponse)
async def get_score(session_id: str):
    """
    Get the current score for a session
    
    Args:
        session_id: User session ID
        
    Returns:
        ScoreResponse with current score information
    """
    try:
        score_response = score_manager.get_score(session_id)
        return score_response
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting score: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get score: {str(e)}")

@app.get("/quiz/session/{session_id}")
async def get_session(session_id: str):
    """
    Get complete session information
    
    Args:
        session_id: User session ID
        
    Returns:
        Dictionary with session summary
    """
    try:
        session_summary = score_manager.get_session_summary(session_id)
        return session_summary
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting session: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get session: {str(e)}")

@app.post("/quiz/reset/{session_id}")
async def reset_session(session_id: str):
    """
    Reset a user session (clear answers and score)
    
    Args:
        session_id: User session ID
        
    Returns:
        Confirmation message
    """
    try:
        score_manager.reset_session(session_id)
        return {"message": "Session reset successfully"}
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error resetting session: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to reset session: {str(e)}")

@app.get("/quiz/leaderboard")
async def get_leaderboard(limit: int = 10):
    """
    Get the leaderboard of top sessions
    
    Args:
        limit: Maximum number of entries to return
        
    Returns:
        List of top sessions
    """
    try:
        leaderboard = score_manager.get_leaderboard(limit)
        return {"leaderboard": leaderboard}
        
    except Exception as e:
        logger.error(f"Error getting leaderboard: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get leaderboard: {str(e)}")

@app.get("/quiz/topics")
async def get_suggested_topics():
    """
    Get a list of suggested topics for quizzes
    
    Returns:
        List of suggested topics
    """
    suggested_topics = [
        "Python Programming",
        "JavaScript Fundamentals",
        "Machine Learning Basics",
        "World History",
        "Biology",
        "Physics",
        "Chemistry",
        "Mathematics",
        "Geography",
        "Literature",
        "Computer Science",
        "Data Structures",
        "Algorithms",
        "Web Development",
        "Artificial Intelligence",
        "Cybersecurity",
        "Climate Change",
        "Space Exploration",
        "Renewable Energy",
        "Quantum Computing"
    ]
    
    return {"suggested_topics": suggested_topics}

@app.post("/quiz/cleanup")
async def cleanup_old_sessions(background_tasks: BackgroundTasks, max_age_hours: int = 24):
    """
    Clean up old sessions (background task)
    
    Args:
        max_age_hours: Maximum age in hours before cleanup
        
    Returns:
        Confirmation message
    """
    def cleanup_task():
        cleaned_count = score_manager.cleanup_old_sessions(max_age_hours)
        logger.info(f"Cleaned up {cleaned_count} old sessions")
    
    background_tasks.add_task(cleanup_task)
    return {"message": "Cleanup task scheduled"}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "status_code": 500}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
