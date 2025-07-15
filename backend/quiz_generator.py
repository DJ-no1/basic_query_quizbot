import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from backend.models import Quiz, QuizQuestion, DifficultyLevel
from typing import List
import json

# Load environment variables
load_dotenv()


class QuizGenerator:
    def __init__(self):
        """Initialize the quiz generator with Google's Generative AI"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.7
        )
        
        # Set up the output parser
        self.output_parser = PydanticOutputParser(pydantic_object=Quiz)
    
    def generate_quiz(self, topic: str, num_questions: int = 5, difficulty: DifficultyLevel = DifficultyLevel.MEDIUM) -> Quiz:
        """
        Generate a quiz on the given topic using structured output
        
        Args:
            topic: The topic for the quiz
            num_questions: Number of questions to generate
            difficulty: Difficulty level of the quiz
            
        Returns:
            Quiz object with structured questions
        """
        
        # Create the prompt template
        prompt_template = """
        You are an expert quiz generator. Create a comprehensive quiz on the given topic.
        
        Topic: {topic}
        Number of questions: {num_questions}
        Difficulty level: {difficulty}
        
        Requirements:
        - Generate exactly {num_questions} multiple choice questions
        - Each question must have exactly 4 options
        - Only one option should be correct
        - Provide clear explanations for correct answers
        - Make questions engaging and educational
        - Vary the difficulty appropriately for {difficulty} level
        - Cover different aspects of the topic
        - Avoid ambiguous questions
        
        For difficulty levels:
        - EASY: Basic concepts, definitions, simple facts
        - MEDIUM: Application of concepts, moderate analysis
        - HARD: Complex analysis, advanced concepts, critical thinking
        
        {format_instructions}
        
        Generate the quiz now:
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["topic", "num_questions", "difficulty"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )
        
        # Format the prompt
        formatted_prompt = prompt.format(
            topic=topic,
            num_questions=num_questions,
            difficulty=difficulty.value
        )
        
        try:
            # Generate the quiz
            response = self.llm.invoke([HumanMessage(content=formatted_prompt)])
            
            # Parse the response
            quiz = self.output_parser.parse(response.content)
            
            # Validate the quiz
            if len(quiz.questions) != num_questions:
                raise ValueError(f"Expected {num_questions} questions, got {len(quiz.questions)}")
            
            # Validate each question
            for i, question in enumerate(quiz.questions):
                if len(question.options) != 4:
                    raise ValueError(f"Question {i+1} must have exactly 4 options")
                if question.correct_answer < 0 or question.correct_answer > 3:
                    raise ValueError(f"Question {i+1} correct_answer must be between 0 and 3")
            
            return quiz
            
        except Exception as e:
            # If parsing fails, try to generate a fallback quiz
            print(f"Error generating quiz: {e}")
            return self._generate_fallback_quiz(topic, num_questions, difficulty)
    
    def _generate_fallback_quiz(self, topic: str, num_questions: int, difficulty: DifficultyLevel) -> Quiz:
        """
        Generate a fallback quiz with basic questions about the topic
        """
        fallback_questions = []
        
        for i in range(num_questions):
            question = QuizQuestion(
                question=f"What is an important concept related to {topic}? (Question {i+1})",
                options=[
                    f"Option A about {topic}",
                    f"Option B about {topic}",
                    f"Option C about {topic}",
                    f"Option D about {topic}"
                ],
                correct_answer=0,
                explanation=f"This is a fallback question about {topic}. Please check your API key and try again.",
                difficulty=difficulty
            )
            fallback_questions.append(question)
        
        return Quiz(
            topic=topic,
            questions=fallback_questions,
            total_questions=num_questions
        )
    
    def validate_quiz(self, quiz: Quiz) -> List[str]:
        """
        Validate a quiz object and return any errors found
        
        Args:
            quiz: The quiz to validate
            
        Returns:
            List of error messages (empty if no errors)
        """
        errors = []
        
        if not quiz.topic or len(quiz.topic.strip()) < 3:
            errors.append("Topic must be at least 3 characters long")
        
        if not quiz.questions:
            errors.append("Quiz must have at least one question")
        
        if quiz.total_questions != len(quiz.questions):
            errors.append("Total questions count doesn't match actual questions")
        
        for i, question in enumerate(quiz.questions):
            if not question.question or len(question.question.strip()) < 5:
                errors.append(f"Question {i+1} must be at least 5 characters long")
            
            if len(question.options) != 4:
                errors.append(f"Question {i+1} must have exactly 4 options")
            
            if question.correct_answer < 0 or question.correct_answer > 3:
                errors.append(f"Question {i+1} correct answer must be between 0 and 3")
            
            if not question.explanation or len(question.explanation.strip()) < 10:
                errors.append(f"Question {i+1} explanation must be at least 10 characters long")
        
        return errors
