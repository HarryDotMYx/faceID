class OverlayRenderer:
    def __init__(self, canvas_context):
        self.ctx = canvas_context
        
    def render_detections(self, faces, canvas_width, canvas_height):
        """Render face detection results on canvas overlay"""
        self.ctx.clearRect(0, 0, canvas_width, canvas_height)
        
        for face in faces:
            self._render_face(face)
            
    def _render_face(self, face):
        """Render a single face detection"""
        is_recognized = face['name'] != 'Unknown'
        
        # Set colors based on recognition status
        stroke_color = '#00ff00' if is_recognized else '#ff0000'
        bg_color = 'rgba(0, 255, 0, 0.2)' if is_recognized else 'rgba(255, 0, 0, 0.2)'
        text_color = '#00ff00' if is_recognized else '#ff0000'
        
        # Draw face rectangle with background
        self.ctx.fillStyle = bg_color
        self.ctx.fillRect(face['x'], face['y'], face['width'], face['height'])
        
        self.ctx.strokeStyle = stroke_color
        self.ctx.lineWidth = 2
        self.ctx.strokeRect(face['x'], face['y'], face['width'], face['height'])
        
        # Draw name label
        label = f"{face['name']} ({face['confidence']}%)" if face['confidence'] else face['name']
        self.ctx.font = '16px Arial'
        text_width = self.ctx.measureText(label).width
        
        # Label background
        self.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)'
        self.ctx.fillRect(face['x'], face['y'] - 25, text_width + 10, 25)
        
        # Label text
        self.ctx.fillStyle = text_color
        self.ctx.fillText(label, face['x'] + 5, face['y'] - 7)