"""
Title: import_albums.py
Purpose: Populate database with music. All available Artist and Album objects can be created through this script
Usage: ./manage.py import_albums

Purpose:
+ clean album & artist strings from file structure names
+ extract track name & number
+ obtain & order track list dictionary
+ store all .mp3 files as tracks
+ store all image files as album artwork
+ store artist's discography
+ instantiate all available Artist objects (to import Tracks, Albums must first be imported.
"""
from .import_artists import get_artist, store_artist_discography
from datasource.models import Album, Artist

from django.conf import settings
from django.core.management.base import BaseCommand

import glob
import os
import re

AUDIO_TYPE = '.mp3'
IMAGE_TYPE = '.gif', '.jpg', '.jpeg', '.png'
PATH = '/argophonica/argophonica/media'
TRACK_NUM_REGEX = '^\d{2}'  # regex of ^start of string, \dArabic numeral, {2}how many chars to count from^


# todo --> either eliminate IMAGE_TYPE ^ or integrate it into glob.glob(*.filetype) below
def get_image(path_string):

    # Set default value for albums without artwork
    album_art = 'No artwork found for this album :('  # put default image here instead

    os.chdir(path_string[0])
    # Check if album directory contains any image files for album artwork
    for file in glob.glob('*.gif') or glob.glob('*.jpg') or glob.glob('*.jpeg') or glob.glob('*.png'):

        # Split PATH on 'media/'
        relative_path = str(path_string[0]).split('media/')
        # Ignore 'media' by using 2nd path because Django MEDIA ROOT adds 'media/' when sending image to browser
        album_art = os.path.join(relative_path[1], file)

        return album_art
    return album_art


def clean_artist_album_names(path_string):

    # Clean artist and album strings, use path length as a marker for cleaning processes
    artist_name = path_string[0][len(PATH):].split('/')[1].replace('_', ' ').title()
    album_name = path_string[0][len(PATH):].split('/')[2].replace('_', ' ').title()

    return artist_name, album_name


def extract_track_name_number(track):

    track_number = str(re.findall(TRACK_NUM_REGEX, track)).strip('[').strip(']').strip("'")
    track_name = track.strip(track_number).strip(AUDIO_TYPE).lstrip().replace('_', ' ').lstrip().title()

    return track_number, track_name


def process_tracks_artwork(path_string):

    # Create dictionary to hold tracks
    track_list = {}

    for track in path_string[2]:  # path_string[2] = files

        # Check for audio files via audio file extension
        if AUDIO_TYPE in track:
            track_number, track_name = extract_track_name_number(track)

            # Add track number to dictionary if it doesn't exist
            if track_number not in track_list.keys():
                track_list[track_number] = track_name

    # Check if album directory contains any image files for album artwork
    album_art = get_image(path_string)

    # Order album by track number
    tracks_sorted = {key: value for key, value in sorted(track_list.items(), key=lambda item: int(item[0]))}

    return album_art, tracks_sorted


def instantiate_album(artist_name, album_name, tracks_sorted, album_art):

    # Create instance with artist because foreign key
    a = Album(artist=Artist.objects.get(artist=artist_name))

    a.title = album_name
    a.release_date = "Not sure ... definitely post-publication of Asimov's first novel!"  # todo: try to get metadata from .mp3 with python lib
    a.genre = 'Not sure ... have a listen & assess!'  # todo: try to get metadata from .mp3 with python lib
    a.number_tracks = len(tracks_sorted)
    a.track_list = tracks_sorted
    a.length = ''  # todo: try to get metadata from .mp3 with python lib
    a.file_type = AUDIO_TYPE
    a.artwork_file = album_art
    a.artwork_link = album_art
    a.notes = ''
    a.save()

    print(f"Saved to database: {a.title} by {a.artist} of filetype {a.file_type}")

    return a


# Search recursively through media directory for all albums
def get_album_data():

    # Structure: path_string[0] = base, [1] = directories, [2] = files.
    # When [1] is len=0, [0] will be path to album directory and [2] will be list of all .mp3 and image files in [0]
    for e, path_string in enumerate(os.walk(PATH)):

        # Check that path_string[1] is empty to stay at consistent level of depth for album data extraction
        if len(path_string[1]) == 0:

            artist_name, album_name = clean_artist_album_names(path_string)

            # Without artist album can't exist -> bound by foreign key. Instantiate artist, pass to Album instantiation
            if Artist.objects.filter(artist=artist_name).exists() is False:
                get_artist(path_string[0], len(PATH))

            # If artist exists but album does not, trigger instantiation
            if Artist.objects.filter(artist=artist_name).exists() and Album.objects.filter(title=album_name).exists() is False:
                album_art, tracks_sorted = process_tracks_artwork(path_string)
                instantiate_album(artist_name, album_name, tracks_sorted, album_art)

            # Check if album is in artist's discography
            store_artist_discography(artist_name, album_name)

    return


class Command(BaseCommand):

    def handle(self, *args, **options):
        print(f'Importing data from {settings.DATA_IMPORT_LOCATION}')
        get_album_data()


if __name__ == '__main__':
    get_album_data()
