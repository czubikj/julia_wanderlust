from django.shortcuts import render

# Create your views here.
def home(request):
    """
    The Blog homepage
    """
    return render(request, 'blog/home.html')