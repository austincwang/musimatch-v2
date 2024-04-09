from django.shortcuts import render

# Create your views here.
def join_game(request):
    return render(request, 'join_game.html')

