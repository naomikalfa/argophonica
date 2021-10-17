from datasource.models import Artist
from django.core.management.base import BaseCommand
import os


def store_artist_discography(artist, album):

    if not Artist.objects.filter(albums__icontains=album):
        artist = Artist.objects.get(artist=artist)

        # None check in place so if this is first album being added we avoid NoneType error and don't store a
        # misplaced comma at the head of the string.
        if artist.albums is None:
            artist.albums = ''
            artist.albums += album
        else:
            # Add album title string with a comma to keep it ordered and to split on it later if needed
            artist.albums += (', ' + album)

        artist.save()

    elif Artist.objects.filter(albums__icontains=album):
        print(f'{album} by {artist} exists, move on.')

    return


def get_artist(path='/argophonica/argophonica/media', path_length=81):

    artists_saved = 0
    for e, path_string in enumerate(os.walk(path)):

        # Clean artist and album strings, use path_length as a marker for cleaning process
        artist_name = path_string[0][path_length:].split('/')[1].replace('_', ' ').title()

        # If artist doesn't exist, create it
        if Artist.objects.filter(artist=artist_name).exists() is False:
            artist = Artist(artist=artist_name)
            artist.save()
            artists_saved += 1
            print(f'{artist_name} was freshly inserted!')

            return artist

    if artists_saved == 0:
        print(f'No new artists to import based on import directory path: {path}')
    else:
        print(f'{artists_saved} new artist(s) imported!')
    return


class Command(BaseCommand):

    def handle(self, *args, **options):
        get_artist()


if __name__ == '__main__':
    get_artist()
