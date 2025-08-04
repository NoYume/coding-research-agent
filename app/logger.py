import time
import threading
import sys
from typing import Optional


class ProgressLogger:
    def __init__(self):
        self.spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        self.spinner_active = False
        self.spinner_thread = None
        self.current_message = ""
    
    
    def start_spinner(self, message:str):
        self.current_message = message
        self.spinner_active = True
        self.spinner_thread = threading.Thread(target=self._spin)
        self.spinner_thread.daemon = True
        self.spinner_thread.start()
        
    
    def stop_spinner(self, completion_message: str =""):
        if not self.spinner_active:
            return
        
        self.spinner_active = False
        if self.spinner_thread:
            self.spinner_thread.join()
        
        sys.stdout.write('\r')
        sys.stdout.write(' ' * 100) 
        sys.stdout.write('\r')
        sys.stdout.flush()
        
        time.sleep(0.02)
        
        if completion_message:
            print(f"✓  {completion_message}")
            sys.stdout.flush()
        
        
    def _spin(self):
        i = 0
        while self.spinner_active:
            if self.spinner_active:
                sys.stdout.write(f"\r{self.spinner_chars[i % len(self.spinner_chars)]} {self.current_message}")
                sys.stdout.flush()
                time.sleep(0.1)
                i += 1
            
    
    def log_step(self, emoji: str, message: str):
        sys.stdout.write("\r")
        print(f"{emoji} {message}")
        sys.stdout.flush()
        
    
    def log_substep(self, message: str, indent: int = 2):
        print(f"{' ' * indent}→ {message}")
    
    
    def log_error(self, message: str, error: Exception = None):
        print(f"❌ {message}")
        if error:
            print(f"   Details: {str(error)}")


    def log_warning(self, message: str):
        print(f"⚠️ {message}")