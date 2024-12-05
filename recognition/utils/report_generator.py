import os
from datetime import datetime
from .docx_generator import DocxGenerator
from ..models import FaceImage
import logging

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self, user):
        self.user = user
        self.doc = DocxGenerator()
        
    def generate_user_report(self):
        """Generate user face recognition report"""
        try:
            # Setup document
            self.doc.add_title('Face Recognition Report')
            
            # Add user information
            self.doc.add_section('User Information', f"""
            Username: {self.user.username}
            Email: {self.user.email}
            Join Date: {self.user.date_joined.strftime('%Y-%m-%d')}
            """)
            
            # Add face images information
            face_images = FaceImage.objects.filter(user=self.user)
            self.doc.add_section('Face Images', f"""
            Total Images: {face_images.count()}
            Last Upload: {face_images.last().uploaded_at.strftime('%Y-%m-%d %H:%M:%S') if face_images else 'N/A'}
            """)
            
            # Add face images table
            headers = ['Image Name', 'Upload Date', 'Status']
            rows = [
                [os.path.basename(img.image.name),
                 img.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
                 'Active']
                for img in face_images
            ]
            self.doc.add_table(headers, rows)
            
            # Save document
            filename = f'user_{self.user.id}_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.docx'
            filepath = self.doc.save(filename)
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return None