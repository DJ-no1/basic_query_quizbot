#!/usr/bin/env python3
"""
Test script to check available Google AI models
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_models():
    """Test available Google AI models"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        return
    
    print(f"🔑 Using API key: {api_key[:10]}...")
    
    # Configure the API
    genai.configure(api_key=api_key)
    
    print("🔍 Checking available models...")
    
    try:
        # List available models
        models = genai.list_models()
        
        print("✅ Available models:")
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(f"  • {model.name} - {model.display_name}")
                print(f"    Supported methods: {model.supported_generation_methods}")
                print()
                
        # Test a simple generation
        print("🧪 Testing model generation...")
        
        # Try different model names
        model_names = [
            "gemini-1.5-flash",
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-pro", 
            "gemini-pro",
            "models/gemini-1.5-flash",
            "models/gemini-1.5-pro",
            "models/gemini-pro"
        ]
        
        for model_name in model_names:
            try:
                print(f"Testing {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("What is machine learning?")
                print(f"✅ {model_name} works!")
                print(f"Response: {response.text[:100]}...")
                break
            except Exception as e:
                print(f"❌ {model_name} failed: {e}")
                
    except Exception as e:
        print(f"❌ Error accessing Google AI: {e}")
        print("Please check your API key and permissions")

if __name__ == "__main__":
    test_models()
