from django.shortcuts import render


def index(request):

    context = {'template': 'about_us',
               'title': 'About Us'}

    return render(request, 'about_us/index.html', context)
