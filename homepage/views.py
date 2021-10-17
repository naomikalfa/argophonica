from django.shortcuts import render


def index(request):

    context = {'template': 'homepage',
               'title': 'Bring it to 11!'}

    return render(request, 'homepage/index.html', context)
