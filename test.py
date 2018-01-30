# shows a user's playlists (need to be authenticated via oauth)

import sys
import spotipy
import spotipy.util as util
import json



def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))


if __name__ == '__main__':
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Whoops, need your username!")
        print("usage: python3 user_playlists.py [username]")
        sys.exit()

    token = util.prompt_for_user_token(username,
                                       client_id=config['SPOTIPY_CLIENT_ID'],
                                       client_secret=config['SPOTIPY_CLIENT_SECRET'],
                                       redirect_uri=config['SPOTIPY_REDIRECT_URI'])

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                print()
                print(playlist['name'])
                print('  total tracks', playlist['tracks']['total'])
                results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
    else:
        print("Can't get token for", username)
