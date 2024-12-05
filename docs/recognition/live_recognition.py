import cv2
import face_recognition
import pickle
import os
import numpy as np
from django.conf import settings
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import time

class LiveRecognition:
    def __init__(self):
        self.current_name = "unknown"
        self.vs = None
        self.fps = None
        self.data = None
        
    def load_encodings(self, user_id):
        """Load face encodings for the user"""
        encoding_path = os.path.join(settings.MEDIA_ROOT, f'encodings/user_{user_id}_encodings.pickle')
        if not os.path.exists(encoding_path):
            return False
        
        print("[INFO] loading encodings...")
        with open(encoding_path, "rb") as f:
            self.data = pickle.loads(f.read())
        return True
            
    def start_stream(self):
        """Initialize video stream"""
        self.vs = VideoStream(src=0, framerate=30).start()
        time.sleep(2.0)  # Allow camera to warm up
        self.fps = FPS().start()
        
    def process_frame(self):
        """Process a single frame from the video stream"""
        frame = self.vs.read()
        if frame is None:
            return None
            
        # Resize frame to speed up processing
        frame = imutils.resize(frame, width=500)
        
        # Detect faces in frame
        boxes = face_recognition.face_locations(frame)
        encodings = face_recognition.face_encodings(frame, boxes)
        names = []
        
        # Process each face found in the frame
        for encoding in encodings:
            matches = face_recognition.compare_faces(
                self.data["encodings"], encoding
            )
            name = "Unknown"
            
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                
                for i in matchedIdxs:
                    name = self.data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                
                name = max(counts, key=counts.get)
                
                if self.current_name != name:
                    self.current_name = name
            
            names.append(name)
        
        # Draw results on frame
        for ((top, right, bottom, left), name) in zip(boxes, names):
            cv2.rectangle(frame, (left, top), (right, bottom),
                (0, 255, 225), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, (0, 255, 255), 2)
        
        self.fps.update()
        return frame
    
    def stop(self):
        """Stop video stream and cleanup"""
        self.fps.stop()
        if self.vs is not None:
            self.vs.stop()
        cv2.destroyAllWindows()