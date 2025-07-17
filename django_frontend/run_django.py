#!/usr/bin/env python
"""Django development server runner for Quiz Bot"""

import os
import sys
import subprocess

def main():
    """Run the Django development server"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quizbot_web.settings')
    
    # Change to the django_frontend directory
    django_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(django_dir)
    
    try:
        # Run migrations
        print("Running Django migrations...")
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        
        # Start the development server
        print("Starting Django development server...")
        print("Django frontend will be available at: http://localhost:8001")
        print("Make sure your FastAPI backend is running on: http://localhost:8000")
        print("\nPress Ctrl+C to stop the server")
        
        subprocess.run([sys.executable, 'manage.py', 'runserver', '8001'])
        
    except subprocess.CalledProcessError as e:
        print(f"Error running Django command: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down Django server...")
        sys.exit(0)

if __name__ == "__main__":
    main()
