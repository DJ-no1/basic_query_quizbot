#!/usr/bin/env python
"""
Complete setup script for Quiz Bot with Django Frontend
Starts both FastAPI backend and Django frontend
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

class QuizBotLauncher:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.project_root = Path(__file__).parent
        
    def start_backend(self):
        """Start the FastAPI backend server"""
        print("🚀 Starting FastAPI Backend...")
        backend_dir = self.project_root / "backend"
        
        try:
            os.chdir(backend_dir)
            self.backend_process = subprocess.Popen([
                sys.executable, "main.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait a bit for the backend to start
            time.sleep(3)
            
            if self.backend_process.poll() is None:
                print("✅ FastAPI Backend started on http://localhost:8000")
                return True
            else:
                print("❌ Failed to start FastAPI Backend")
                return False
                
        except Exception as e:
            print(f"❌ Error starting backend: {e}")
            return False
    
    def start_frontend(self):
        """Start the Django frontend server"""
        print("🚀 Starting Django Frontend...")
        frontend_dir = self.project_root / "django_frontend"
        
        try:
            os.chdir(frontend_dir)
            
            # Run migrations first
            print("Running Django migrations...")
            migration_result = subprocess.run([
                sys.executable, "manage.py", "migrate"
            ], capture_output=True, text=True)
            
            if migration_result.returncode != 0:
                print(f"⚠️  Migration warning: {migration_result.stderr}")
            
            # Start Django server
            self.frontend_process = subprocess.Popen([
                sys.executable, "manage.py", "runserver", "8001"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait a bit for the frontend to start
            time.sleep(3)
            
            if self.frontend_process.poll() is None:
                print("✅ Django Frontend started on http://localhost:8001")
                return True
            else:
                print("❌ Failed to start Django Frontend")
                return False
                
        except Exception as e:
            print(f"❌ Error starting frontend: {e}")
            return False
    
    def monitor_processes(self):
        """Monitor both processes and show their output"""
        def read_output(process, name):
            while process and process.poll() is None:
                try:
                    line = process.stdout.readline()
                    if line:
                        print(f"[{name}] {line.strip()}")
                except:
                    break
        
        if self.backend_process:
            backend_thread = threading.Thread(
                target=read_output, 
                args=(self.backend_process, "Backend"),
                daemon=True
            )
            backend_thread.start()
        
        if self.frontend_process:
            frontend_thread = threading.Thread(
                target=read_output, 
                args=(self.frontend_process, "Frontend"),
                daemon=True
            )
            frontend_thread.start()
    
    def stop_servers(self):
        """Stop both servers"""
        print("\n🛑 Stopping servers...")
        
        if self.backend_process:
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
                print("✅ Backend stopped")
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
                print("🔪 Backend force killed")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend stopped")
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
                print("🔪 Frontend force killed")
    
    def run(self):
        """Main run method"""
        print("🎯 Quiz Bot Launcher")
        print("=" * 50)
        
        # Setup signal handler for graceful shutdown
        def signal_handler(signum, frame):
            self.stop_servers()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start backend
        if not self.start_backend():
            print("❌ Failed to start backend. Exiting.")
            return
        
        # Start frontend
        if not self.start_frontend():
            print("❌ Failed to start frontend. Stopping backend.")
            self.stop_servers()
            return
        
        print("\n" + "=" * 50)
        print("🎉 Both servers are running!")
        print("📱 Django Frontend: http://localhost:8001")
        print("🔧 FastAPI Backend:  http://localhost:8000")
        print("📚 API Docs:         http://localhost:8000/docs")
        print("\n💡 Make sure you have your .env file with GOOGLE_API_KEY")
        print("⚡ Press Ctrl+C to stop both servers")
        print("=" * 50)
        
        # Monitor processes
        self.monitor_processes()
        
        try:
            # Wait for processes to end
            while (self.backend_process and self.backend_process.poll() is None) or \
                  (self.frontend_process and self.frontend_process.poll() is None):
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_servers()

if __name__ == "__main__":
    launcher = QuizBotLauncher()
    launcher.run()
