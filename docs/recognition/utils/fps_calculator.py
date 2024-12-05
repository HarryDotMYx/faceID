import time

class FPSCalculator:
    def __init__(self, update_interval=30):
        self.frame_count = 0
        self.fps = 0
        self.start_time = None
        self.update_interval = update_interval
        
    def update(self):
        """Update FPS calculation"""
        if self.start_time is None:
            self.start_time = time.time()
            
        self.frame_count += 1
        
        if self.frame_count >= self.update_interval:
            elapsed_time = time.time() - self.start_time
            self.fps = round(self.frame_count / elapsed_time)
            self.frame_count = 0
            self.start_time = time.time()
            
    def get_fps(self):
        """Get current FPS value"""
        return self.fps