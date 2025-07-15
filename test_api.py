#!/usr/bin/env python3
"""
Test script for QuizBot API

This script tests the basic functionality of the QuizBot API.
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

class QuizBotTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id = None
    
    async def test_health_check(self, session: aiohttp.ClientSession) -> bool:
        """Test the health check endpoint"""
        try:
            async with session.get(f"{self.base_url}/health") as response:
                data = await response.json()
                print(f"✅ Health Check: {data['status']}")
                return data['status'] == 'healthy'
        except Exception as e:
            print(f"❌ Health Check Failed: {e}")
            return False
    
    async def test_generate_quiz(self, session: aiohttp.ClientSession, topic: str = "Python Programming") -> Dict[Any, Any]:
        """Test quiz generation"""
        try:
            payload = {
                "topic": topic,
                "num_questions": 3,
                "difficulty": "medium"
            }
            
            async with session.post(f"{self.base_url}/quiz/generate", json=payload) as response:
                data = await response.json()
                
                if data.get('success'):
                    self.session_id = data['session_id']
                    print(f"✅ Quiz Generated: {data['quiz']['topic']}")
                    print(f"   Questions: {data['quiz']['total_questions']}")
                    print(f"   Session ID: {self.session_id}")
                    return data
                else:
                    print(f"❌ Quiz Generation Failed: {data.get('error', 'Unknown error')}")
                    return {}
        except Exception as e:
            print(f"❌ Quiz Generation Error: {e}")
            return {}
    
    async def test_submit_answer(self, session: aiohttp.ClientSession, question_index: int = 0, selected_option: int = 0) -> Dict[Any, Any]:
        """Test answer submission"""
        if not self.session_id:
            print("❌ No session ID available for answer submission")
            return {}
        
        try:
            payload = {
                "question_index": question_index,
                "selected_option": selected_option
            }
            
            async with session.post(f"{self.base_url}/quiz/answer?session_id={self.session_id}", json=payload) as response:
                data = await response.json()
                
                result = "✅ Correct" if data.get('correct') else "❌ Incorrect"
                print(f"{result} Answer: Question {question_index + 1}")
                print(f"   Score Change: {data.get('score_change', 0)}")
                return data
        except Exception as e:
            print(f"❌ Answer Submission Error: {e}")
            return {}
    
    async def test_get_score(self, session: aiohttp.ClientSession) -> Dict[Any, Any]:
        """Test score retrieval"""
        if not self.session_id:
            print("❌ No session ID available for score retrieval")
            return {}
        
        try:
            async with session.get(f"{self.base_url}/quiz/score/{self.session_id}") as response:
                data = await response.json()
                
                print(f"✅ Score Retrieved:")
                print(f"   Current Score: {data.get('current_score', 0)}")
                print(f"   Correct: {data.get('correct_answers', 0)}")
                print(f"   Incorrect: {data.get('incorrect_answers', 0)}")
                print(f"   Percentage: {data.get('percentage', 0):.1f}%")
                return data
        except Exception as e:
            print(f"❌ Score Retrieval Error: {e}")
            return {}
    
    async def test_suggested_topics(self, session: aiohttp.ClientSession) -> Dict[Any, Any]:
        """Test suggested topics endpoint"""
        try:
            async with session.get(f"{self.base_url}/quiz/topics") as response:
                data = await response.json()
                
                print(f"✅ Suggested Topics: {len(data.get('suggested_topics', []))} topics")
                return data
        except Exception as e:
            print(f"❌ Suggested Topics Error: {e}")
            return {}
    
    async def run_tests(self):
        """Run all tests"""
        print("🧪 Starting QuizBot API Tests...")
        print("=" * 50)
        
        async with aiohttp.ClientSession() as session:
            # Test health check
            if not await self.test_health_check(session):
                print("❌ Server is not healthy. Stopping tests.")
                return
            
            print()
            
            # Test suggested topics
            await self.test_suggested_topics(session)
            print()
            
            # Test quiz generation
            quiz_data = await self.test_generate_quiz(session)
            if not quiz_data:
                print("❌ Cannot continue without a valid quiz")
                return
            
            print()
            
            # Test answer submission for first question
            await self.test_submit_answer(session, 0, 0)
            print()
            
            # Test score retrieval
            await self.test_get_score(session)
            print()
            
            print("=" * 50)
            print("🎉 All tests completed!")

async def main():
    """Main function to run tests"""
    tester = QuizBotTester()
    await tester.run_tests()

if __name__ == "__main__":
    asyncio.run(main())
