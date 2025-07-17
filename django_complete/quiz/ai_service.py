"""
AI Quiz Generation Service for Django
Integrates LangChain with Google Generative AI for quiz creation
"""

import os
from typing import List, Dict, Any
from django.conf import settings
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from pydantic import BaseModel, Field


class QuizQuestionPydantic(BaseModel):
    """Pydantic model for quiz question validation"""
    question: str = Field(description="The quiz question")
    option_a: str = Field(description="Option A")
    option_b: str = Field(description="Option B") 
    option_c: str = Field(description="Option C")
    option_d: str = Field(description="Option D")
    correct_answer: int = Field(description="Correct answer index (0-3)", ge=0, le=3)
    explanation: str = Field(description="Explanation for the correct answer")
    difficulty: str = Field(description="Question difficulty level")


class QuizPydantic(BaseModel):
    """Pydantic model for complete quiz validation"""
    topic: str = Field(description="Quiz topic")
    difficulty: str = Field(description="Overall difficulty level")
    questions: List[QuizQuestionPydantic] = Field(description="List of quiz questions")


class AIQuizService:
    """Service class for AI-powered quiz generation"""
    
    def __init__(self):
        self.setup_ai()
    
    def setup_ai(self):
        """Initialize Google Generative AI"""
        try:
            # Configure the API key
            api_key = getattr(settings, 'GOOGLE_GENERATIVE_AI_API_KEY', None)
            if not api_key:
                # Try environment variable
                api_key = os.getenv('GOOGLE_GENERATIVE_AI_API_KEY')
            
            if not api_key:
                raise ValueError("Google Generative AI API key not found in settings or environment")
            
            genai.configure(api_key=api_key)
            
            # Initialize LangChain LLM
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0.7
            )
            
            # Setup output parser
            self.output_parser = PydanticOutputParser(pydantic_object=QuizPydantic)
            
        except Exception as e:
            print(f"Error setting up AI service: {e}")
            raise
    
    def generate_quiz_prompt(self, topic: str, difficulty: str, num_questions: int) -> str:
        """Generate the prompt for quiz creation"""
        
        difficulty_instructions = {
            "easy": "Make questions straightforward with basic concepts and clear answers.",
            "medium": "Include questions that require some analysis and understanding of concepts.",
            "hard": "Create challenging questions that require deep understanding and critical thinking."
        }
        
        prompt = f"""Create a quiz about "{topic}" with {num_questions} multiple choice questions.

Difficulty Level: {difficulty}
{difficulty_instructions.get(difficulty, "Use medium difficulty level.")}

Requirements:
1. Each question should have exactly 4 options (A, B, C, D)
2. Only one option should be correct
3. Provide a clear explanation for the correct answer
4. Make sure questions are relevant to the topic
5. Vary the difficulty within the specified level
6. Use clear, unambiguous language

Please respond with a JSON object in this exact format:
{{
  "topic": "{topic}",
  "difficulty": "{difficulty}",
  "questions": [
    {{
      "question": "Your question here",
      "option_a": "First option",
      "option_b": "Second option", 
      "option_c": "Third option",
      "option_d": "Fourth option",
      "correct_answer": 0,
      "explanation": "Explanation for the correct answer",
      "difficulty": "{difficulty}"
    }}
  ]
}}

Generate the quiz now:"""
        
        return prompt
    
    def generate_quiz(self, topic: str, difficulty: str = "medium", num_questions: int = 10) -> QuizPydantic:
        """Generate a complete quiz using AI"""
        try:
            # Create the prompt
            prompt = self.generate_quiz_prompt(topic, difficulty, num_questions)
            
            # Generate response using LLM directly
            response = self.llm.invoke(prompt)
            
            # Parse the response content
            if hasattr(response, 'content'):
                content = response.content
            else:
                content = str(response)
            
            # Try to extract JSON from the response
            import json
            import re
            
            # Look for JSON object in the response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                quiz_data = json.loads(json_str)
                
                # Validate and create QuizPydantic object
                return QuizPydantic(**quiz_data)
            else:
                # If no JSON found, return fallback
                return self.create_fallback_quiz(topic, difficulty, num_questions)
            
        except Exception as e:
            print(f"Error generating quiz: {e}")
            # Return a fallback quiz structure
            return self.create_fallback_quiz(topic, difficulty, num_questions)
    
    def create_fallback_quiz(self, topic: str, difficulty: str, num_questions: int) -> QuizPydantic:
        """Create a basic fallback quiz if AI generation fails"""
        questions = []
        
        for i in range(min(num_questions, 3)):  # Limit fallback questions
            question = QuizQuestionPydantic(
                question=f"Sample question {i+1} about {topic}",
                option_a="Option A",
                option_b="Option B", 
                option_c="Option C",
                option_d="Option D",
                correct_answer=0,
                explanation=f"This is a sample explanation for question {i+1}",
                difficulty=difficulty
            )
            questions.append(question)
        
        return QuizPydantic(
            topic=topic,
            difficulty=difficulty,
            questions=questions
        )
    
    def validate_quiz_data(self, quiz_data: Dict[str, Any]) -> QuizPydantic:
        """Validate quiz data using Pydantic"""
        try:
            return QuizPydantic(**quiz_data)
        except Exception as e:
            print(f"Validation error: {e}")
            raise ValueError(f"Invalid quiz data: {e}")


# Global instance
ai_quiz_service = AIQuizService()
