import random
import spotipy
from os import path
import configparser


def shufflePlaylist(playlistURI):
    # getting the default cache path (from spotshuffle)
    scriptPath = path.dirname(path.realpath(__file__))
    cachePath = scriptPath+'/spotifytokencache'

    scope = 'user-library-read playlist-modify-public playlist-modify-private'

    config = configparser.ConfigParser()
    config.read(scriptPath+'/config.cfg')

    # making sure authorization token is present to avoid making user login
    if not path.isfile(cachePath):
        print("Cached authorization token not found, please run spotshuffle program first.")
        exit(1)

    # Tries to authorize the user with cached token
    try:
        spotify = spotipy.Spotify(
            auth_manager=spotipy.oauth2.SpotifyOAuth(
                client_id=config.get('APPDATA', 'CLIENT_ID'),
                client_secret=config.get('APPDATA', 'CLIENT_SECRET'),
                redirect_uri=config.get('APPDATA', 'REDIRECT_URI'),
                scope=scope,
                cache_path=cachePath
            )
        )
    except spotipy.oauth2.SpotifyOauthError:
        print("Unable to obtain Spotify permissions with cached token")
        exit(1)

    songIDList = []
    playlistURI = "spotify:playlist:6cDcezvYjrKXi8B7UIJLaP"

    # retrieve all tracks in the playlist
    playlistContents = spotify.playlist_items(playlistURI)
    for song in playlistContents['items']:
        songIDList.append(song['track']['id'])

    # shuffle the tracks and save it
    random.shuffle(songIDList)

    spotify.playlist_replace_items(playlistURI, songIDList)