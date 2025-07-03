from django.shortcuts import render

def home(request):
    """
    Render the home page of the CRM application.
    
    Args:
        request: The HTTP request object.
    
    Returns:
        HttpResponse: Rendered home page template.
    """
    return render(request, 'index.html')
