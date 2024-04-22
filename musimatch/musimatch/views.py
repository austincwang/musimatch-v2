from django.shortcuts import render

def homepage(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def error(request, error):
    context = {}
    context['error'] = error
    return render(request, 'error_screen.html', context)