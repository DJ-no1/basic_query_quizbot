from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuizQuestion(BaseModel):
    """Individual quiz question with 4 multiple choice options"""
    question: str = Field(..., description="The quiz question")
    options: List[str] = Field(..., description="Four multiple choice options", min_items=4, max_items=4)
    correct_answer: int = Field(..., description="Index of the correct answer (0-3)", ge=0, le=3)
    explanation: str = Field(..., description="Explanation of why this is the correct answer")
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.MEDIUM, description="Difficulty level of the question")


class Quiz(BaseModel):
    """Complete quiz with multiple questions"""
    topic: str = Field(..., description="The topic of the quiz")
    questions: List[QuizQuestion] = Field(..., description="List of quiz questions", min_items=1)
    total_questions: int = Field(..., description="Total number of questions in the quiz")
    
    def model_post_init(self, __context) -> None:
        """Automatically set total_questions based on the questions list"""
        self.total_questions = len(self.questions)


class QuizRequest(BaseModel):
    """Request model for generating a quiz"""
    topic: str = Field(..., description="Topic for the quiz", min_length=3)
    num_questions: int = Field(default=5, description="Number of questions to generate", ge=1, le=20)
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.MEDIUM, description="Difficulty level")


class QuizResponse(BaseModel):
    """Response model for quiz generation"""
    success: bool
    quiz: Optional[Quiz] = None
    error: Optional[str] = None


class AnswerRequest(BaseModel):
    """Request model for submitting an answer"""
    question_index: int = Field(..., description="Index of the question being answered", ge=0)
    selected_option: int = Field(..., description="Index of the selected option (0-3)", ge=0, le=3)


class AnswerResponse(BaseModel):
    """Response model for answer submission"""
    correct: bool
    correct_answer: int
    explanation: str
    score_change: int  # Points gained or lost


class ScoreResponse(BaseModel):
    """Response model for score tracking"""
    current_score: int
    total_questions_answered: int
    correct_answers: int
    incorrect_answers: int
    percentage: float
