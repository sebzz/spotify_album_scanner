import os
import logging

import mutagen


def get_all_albums(directory):
    artist_albums = {_album_name_from_file(file_name) for file_name
                     in _all_file_names(directory)}
    artist_albums.discard(None)
    return artist_albums


def _album_name_from_file(file_name):
    try:
        result = mutagen.File(file_name)
    except KeyError as e:
        logging.error("Couldn't read album name for file %s: %s" % (file_name, e))
        return None

    if result:
        artist = result.tags.get('artist')
        album = result.tags.get('album')
        if artist and artist[0] and album and album[0]:
            return (artist[0], album[0])
        else:
            logging.error("Couldn't read album name for file %s" % file_name)
            return None


def _all_file_names(directory):
    files = []
    for root, dirs, files in os.walk(directory):
        full_path_names = (os.path.join(root, f) for f in files)
        file_names = (file_name for file_name
                      in full_path_names if os.path.isfile(file_name))
        for f in file_names:
            yield f
