#!/usr/bin/env python3
"""
QuizBot - AI-Powered Quiz Generator

This script starts the QuizBot backend server.
Make sure to set up your Google API key in the .env file before running.
"""

import os
import sys
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Main entry point for the application"""
    # Check if Google API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY not found in environment variables.")
        print("Please:")
        print("1. Copy .env.example to .env")
        print("2. Add your Google API key to the .env file")
        print("3. Run the script again")
        sys.exit(1)
    
    print("🚀 Starting QuizBot Backend Server...")
    print("📡 API will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🔄 To stop the server, press Ctrl+C")
    
    # Start the server
    try:
        uvicorn.run(
            "backend.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=["backend"],
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 QuizBot server stopped.")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
