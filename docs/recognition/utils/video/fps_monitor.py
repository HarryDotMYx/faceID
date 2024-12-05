import time

class FPSMonitor:
    def __init__(self, update_interval=1000):
        self.frame_count = 0
        self.last_time = time.time() * 1000  # Convert to milliseconds
        self.fps = 0
        self.update_interval = update_interval
        
    def update(self):
        """Update FPS calculation"""
        self.frame_count += 1
        current_time = time.time() * 1000
        elapsed = current_time - self.last_time
        
        if elapsed >= self.update_interval:
            self.fps = round((self.frame_count * 1000) / elapsed)
            self.frame_count = 0
            self.last_time = current_time
            
    def get_fps(self):
        """Get current FPS value"""
        return self.fps