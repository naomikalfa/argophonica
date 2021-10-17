from django.shortcuts import render
from django.views.generic.detail import DetailView

from datasource.models import Album, Track


class AlbumDetailView(DetailView):

    model = Album
    template_name = 'album_view.html'

    def get_context_data(self, **kwargs):

        context = super(AlbumDetailView, self).get_context_data(**kwargs)

        next_album = Album.objects.filter(title__gt=self.object.title).order_by('title').first()
        prev_album = Album.objects.filter(title__lt=self.object.title).order_by('-title').first()

        # Cyclically retrieve first and last albums to loop through album list
        if next_album is None:
            next_album = Album.objects.order_by('title').first()
        if prev_album is None:
            prev_album = Album.objects.order_by('-title').first()

        context['next_album'] = next_album
        context['prev_album'] = prev_album
        context['track'] = Track.objects.filter(album=self.object).order_by('track_number')

        return context


def index(request):

    context = dict(template='album_index',
                   title='Musicplayer index',
                   description='|  A R G O P H O N I C A   | \n\n'
                               '| a  r  t  i  s  t  s |'
                               '\n\n')

    # todo --> Work out why calling order_by isn't sorting alphabetically! The dis-order is driving me nuts!
    # Retrieve and neatly label list of each artist with their albums for template display and slug linking purposes
    display_index_albums = {}
    albums = Album.objects.distinct('artist').order_by('artist')

    for album in albums:
        artist_key = album.track_set.core_filters['album'].artist.artist

        album_list = Album.objects.filter(artist=album.artist)

        for e, a in enumerate(album_list):
            # This form of query is used so values are stripped of all unwanted "QuerySet<[]>" characters when rendered
            slug = a.track_set.core_filters['album'].slug
            title = a.track_set.core_filters['album'].title
            album_title = {'title': title,
                           'slug': slug}

            # Formulate dicts thusly to avoid overwriting artist's album keys if artist has multiple albums
            if artist_key in display_index_albums:
                display_index_albums[artist_key].update([(e, album_title)])
            else:
                display_index_albums[artist_key] = {}
                display_index_albums[artist_key].update([(e, album_title)])

    context['display_index_albums'] = display_index_albums

    return render(request, 'album_index.html', context)
