from .import_albums import clean_artist_album_names, extract_track_name_number
from datasource.models import Album, Artist, Track

from django.conf import settings
from django.core.management.base import BaseCommand

import glob
import os

PATH = '/argophonica/argophonica/media'


def construct_audio_link(path_string, track_number, track_name):
    # We construct the link like this because if we just pass in a path_string to process, each time a new track calls
    # this function it will always start at path_string[2][0] and store that track as audio_field instead of its true
    # file. Disaster! Avoid!

    os.chdir(path_string[0])
    # Check if album dir contains any audio files. Specifying file type to ignore image files
    for _ in glob.glob('*.mp3'):

        # Split PATH on 'media/'
        relative_path = str(path_string[0]).split('media/')

        # Ignore 'media' by using 2nd path bc Django MEDIA ROOT handles adding 'media/' when sending image to browser
        # Else the URL path will be incorrect
        audio_file = os.path.join(relative_path[1], track_number + ' ' + track_name + '.mp3')

        return audio_file


def get_track(audio_type='.mp3'):

    tracks_saved = 0

    for e, path_string in enumerate(os.walk(PATH)):

        # Check that path_string[1] is empty to stay at consistent level of depth for album data extraction
        if len(path_string[1]) == 0:
            # Clean artist and album strings
            artist_name, album_name = clean_artist_album_names(path_string)

            # Get remainder of data
            for track in path_string[2]:  # path_string[2] = files

                # Check for audio files via audio file extension
                if audio_type in track:

                    # Extract track info from path string
                    track_number, track_name = extract_track_name_number(track)

                    # Extract audio file from path string
                    audio_file = construct_audio_link(path_string, track_number, track_name)

                    # If track exists then pass, else begin instantiation of tracks
                    if Track.objects.filter(title=track_name, artist=artist_name).exists():
                        print(f'Passing, the track {track_name} already exists.')

                    else:
                        # Need to create instance with Album and Artist preloaded because foreign key
                        t = Track(album=Album.objects.get(title=album_name), artist=Artist.objects.get(artist=artist_name))
                        t.title = track_name
                        t.length = 'Not sure ... have a listen and time it'
                        t.track_number = track_number
                        t.audio_file = audio_file
                        t.audio_link = audio_file
                        t.save()
                        print(f"Saved to database: {t.title} link {t.audio_file} by {t.artist} off the album {t.album}")
                        tracks_saved += 1

    print(f'{tracks_saved} tracks saved to database.')
    return


class Command(BaseCommand):

    def handle(self, *args, **options):
        print(f'Importing data from {settings.DATA_IMPORT_LOCATION}')
        get_track()


if __name__ == '__main__':
    get_track()
