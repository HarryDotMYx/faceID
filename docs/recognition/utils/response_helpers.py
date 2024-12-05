from django.http import JsonResponse

def error_response(message, status=400):
    """Create a standardized error response"""
    return JsonResponse({
        'success': False,
        'error': message
    }, status=status)

def success_response(data, status=200):
    """Create a standardized success response"""
    response_data = {
        'success': True
    }
    response_data.update(data)
    return JsonResponse(response_data, status=status)