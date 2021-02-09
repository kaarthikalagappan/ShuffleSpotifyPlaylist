from os import path
import random
import spotipy
import configparser

scriptPath = path.dirname(path.realpath(__file__))
cachePath = scriptPath+'/spotifytokencache'

scope = 'playlist-modify-public playlist-modify-private'

config = configparser.ConfigParser()
config.read(scriptPath+'/config.cfg')

spotify = spotipy.Spotify(
    auth_manager=spotipy.oauth2.SpotifyOAuth(
        client_id=config.get('APPDATA', 'CLIENT_ID'),
        client_secret=config.get('APPDATA', 'CLIENT_SECRET'),
        redirect_uri=config.get('APPDATA', 'REDIRECT_URI'),
        scope=scope,
        cache_path=cachePath,
        open_browser=False
    )
)

playlistURI = config.get('PLAYLIST', 'ID')
songIDList = []

playlistContents = spotify.playlist_items(playlistURI)
for song in playlistContents['items']:
    songIDList.append(song['track']['id'])

random.shuffle(songIDList)

spotify.playlist_replace_items(playlistURI, songIDList)