import logging

import spotipy
import spotipy.util as util


def auth(username):
    token = util.prompt_for_user_token(username, "user-library-modify")
    return Spotify(token)


class Spotify(object):

    def __init__(self, token):
        self.token = token
        self.spotify = spotipy.Spotify(auth=token)

    def add_album(self, artist, album):
        album = self._search_album(artist, album)
        if album:
          tracks = self._album_tracks(album)
          self._save_tracks(tracks)

    def _search_album(self, artist, album):
        query = 'artist:%s album:%s' % (artist, album)
        response = self.spotify.search(q=query, limit=1, type='album')
        album_data = response['albums']['items']
        if not album_data:
            logging.warn("Couldn't find album %s" % album)
            return None
        else:
            return album_data[0]

    def _album_tracks(self, album):
        return self.spotify.album_tracks(album['id'])['items']

    def _save_tracks(self, tracks):
        track_ids = (track['id'] for track in tracks)
        response = self.spotify.current_user_saved_tracks_add(track_ids)
        print response
