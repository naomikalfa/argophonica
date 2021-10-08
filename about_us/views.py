from django.shortcuts import render


def index(request):
    context = {'template': 'about_us',
               'title': 'About Us',
               'description': 'We present to you Argophonica, a site to sate your cochleae!\n\n'
                              'Whence comes our name? Read on, fair listener.\n\n'
                              '\nIn "Metamporphoses" Book 11, Ovid writes of Orpheus: \n'
                              '"With his songs, Orpheus, the bard of Thrace, allured the trees, the savage animals, '
                              'and even the insensate rocks, to follow him."\n'         
                              '\n+\n\n'
                              'Before the Latin writings came the Greek writings.\n'
                              'One of its epics, "Argonautica Orphica", is narrated by the voice of Orpheus. It is '
                              'herein claimed that the Argo was the first ship ever built. It had many splendorous '
                              '& terrifying adventures, one of which was its encounter with the overwhelming sounds ' 
                              'of the Sirens, as the Argonauts carried out their quest to bring the Golden Fleece to '
                              'Iolcus.\n'
                              '\n+\n\n'
                              'The adjective "phonic", denoting that which pertains to sound, comes to us through the '
                              'Greek phōnē which denotes sound or voice.\n'
                              '\n=\n\n'
                              'Argophonica!\n\n'
                              '\nMay the music be as a voyage to you, a quest, an epic to traverse!\n\n'}

    return render(request, 'about_us/index.html', context)
