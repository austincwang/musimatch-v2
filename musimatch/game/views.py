from django.shortcuts import render

# Create your views here.
def join_game(request):
    context = {}
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    context['things'] = list
    return render(request, 'join_game.html', context)

