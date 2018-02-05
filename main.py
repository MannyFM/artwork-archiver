import json
import sys
from typing import List

import spotipy
import spotipy.util as util

from models import normalize_album

sp = None


def show_tracks(tracks: dict):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %2d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))


def show_albums_json(albums: list):
    for i, item in enumerate(albums):
        # album = item['album']
        album = item
        print("   %2d %32.32s %s" % (i, album['artists'][0]['name'], album['name']))


def show_albums(albums: List[tuple]):
    for i, item in enumerate(albums):
        print("   %2d %32.32s %s" % (i, item[0], item[1]))


def get_all_saved_albums():
    global sp
    albums = []
    results = sp.current_user_saved_albums()
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        # albums.extend(normalize_album(results['items']))
        albums.extend(results['items'])
    return albums


def get_albums_from_tracks(max_album_count: int = 200) -> List[tuple]:
    global sp
    # albums = []
    results = sp.current_user_saved_tracks(limit=50)
    results_set = set()
    total = 0

    for item in results['items']:
        cur = item['track']['album']
        album = normalize_album(cur)
        # albums.append(cur)
        results_set.add(album)
        total += 1

    while results['next']:
        if results['offset'] > max_album_count:
            break
        print("\r{}/{}".format(results['offset'], max_album_count), end="")
        results = sp.next(results)
        for item in results['items']:
            cur = item['track']['album']
            album = normalize_album(cur)
            # albums.append(cur)
            results_set.add(album)
            total += 1
    # print(len(albums))
    # print(len(results_set))
    print("\rThere was total {} tracks and set is {} length".format(total, len(results_set)))
    return list(results_set)
    # return albums


def main():
    global sp
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Whoops, need your username!")
        print("usage: python3 user_playlists.py [username]")

        username = input("Enter username or nothing to exit:")
        if username == "":
            sys.exit()

    scope = 'user-library-read'
    token = util.prompt_for_user_token(username, scope,
                                       client_id=config['SPOTIPY_CLIENT_ID'],
                                       client_secret=config['SPOTIPY_CLIENT_SECRET'],
                                       redirect_uri=config['SPOTIPY_REDIRECT_URI'])

    if token:
        sp = spotipy.Spotify(auth=token)
        albums = get_albums_from_tracks(max_album_count=200)
        # print(len(albums))
        # show_albums(albums)
        with open('dump.json', 'w') as fp:
            json.dump(albums, fp)
            # json.dump(albums, fp, iterable_as_array=True)
    else:
        print("Can't get token for", username)


if __name__ == '__main__':
    print("Script is started")
    main()
    print("Script ended")
