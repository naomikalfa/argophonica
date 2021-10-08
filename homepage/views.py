from django.shortcuts import render


def index(request):
    context = {'template': 'homepage',
               'title': 'Bring it to 11!',
               'description': 'You\'ve arrived! Thanks for stopping by, awful kind of you.'
                              '\nNigel wants to know if we can get this music up to the hallowed '
                              'heights of 11 !'}
    return render(request, 'homepage/index.html', context)
