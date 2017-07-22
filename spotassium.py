import sys
import spotipy
import spotipy.util as util
import confuse
import time

from itertools import groupby
from subprocess import call

from player import is_playing

config = confuse.Configuration('spotassium', __name__)
config.add({
    'spotify_app_key': '',
    'playlist_name': '',
    'verbose': False,
})
WAIT_PERIOD = 300  # 5 min


def run_command_on_spotify_id(spotify_id):
    """Run external command on given track id"""
    placeholder = '<SPOTIFY_ID>'
    print(config['command'].get())
    cmd = config['command'].get().replace(placeholder, spotify_id)
    call(cmd.split(' '))


def do_playlist(playlist_id):
    """Iterate on every track of playlist to run command on it.
       Remove track from playlist if command successful.
    """
    results = sp.user_playlist(username, playlist_id,
                               fields="tracks,next")
    for album, tracks in groupby(results['tracks']['items'],
                                 key=lambda x: x['track']['album']['uri']):
        for track in list(tracks):
            run_command_on_spotify_id(track['track']['uri'])
            # sp.user_playlist_remove_all_occurrences_of_tracks(username,
            #     playlist_id, [track['track']['id'],])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print "Whoops, need your username!"
        print "usage: python user_playlists.py [username]"
        sys.exit()

    token = util.prompt_for_user_token(username, 'playlist-modify-public')

    if token:
        print('Access token: %s' % token)
        sp = spotipy.Spotify(auth=token)

        playlists = sp.user_playlists(username)['items']
        while True:
            if not is_playing():
                for playlist in playlists:
                    if playlist['name'] == config['playlist_name'].get():
                        do_playlist(playlist['id'])
            time.sleep(WAIT_PERIOD)
    else:
        print "Can't get token for", username
