from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from ..utils.report_generator import ReportGenerator
import os
import logging

logger = logging.getLogger(__name__)

@login_required
def generate_report(request):
    """Generate and download user report"""
    try:
        generator = ReportGenerator(request.user)
        filepath = generator.generate_user_report()
        
        if filepath and os.path.exists(filepath):
            response = FileResponse(
                open(filepath, 'rb'),
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(filepath)}"'
            return response
            
        raise Http404("Report generation failed")
        
    except Exception as e:
        logger.error(f"Error in report view: {str(e)}")
        raise Http404("Report generation failed")