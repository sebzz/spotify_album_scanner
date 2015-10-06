import logging
import sys

import local_music
import spotify


def run(args):
    if len(args) != 3:
        print "Usage: %s username dir" % (args,)
        sys.exit()

    logger = _get_logger()

    username = sys.argv[1]
    directory = sys.argv[2]

    spotify_client = spotify.auth(username)

    local_albums = local_music.get_all_albums(directory)
    for (artist, album) in sorted(local_albums):
        logger.info("Importing %s %s" % (artist, album))
        spotify_client.add_album(artist, album)


def _get_logger():
    logger = logging.getLogger('track_saver')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

if __name__ == '__main__':
    run(sys.argv)
