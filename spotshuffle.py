from os import path
import random
import spotipy
import configparser

# cache the authorization token to avoid authorizing everytime
scriptPath = path.dirname(path.realpath(__file__))
cachePath = scriptPath+'/spotifytokencache'

scope = 'user-library-read playlist-modify-public playlist-modify-private'

config = configparser.ConfigParser()
config.read(scriptPath+'/config.cfg')

# Tries to authorize the user with the given crendtials
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
    print("Unable to obtain Spotify permissions")
    exit(1)

# Get the current user's playlist
results = spotify.current_user_playlists()

# Print out the playlists and assign them numbers
for counter, item in enumerate(results['items']):
    print('[' + str(counter+1) + "] " + item['name'])

# Ask user which playlist to shuffle
playlist_to_shuffle = input("Which playlist to shuffle (1-" + str(len(results['items'])) + ")? ")

# Validate the chosen option
while (playlist_to_shuffle is (not playlist_to_shuffle.isdigit())) \
       or (int(playlist_to_shuffle) < 1 
       or int(playlist_to_shuffle) > len(results['items'])):
    playlist_to_shuffle = input("Invalid input. Please enter a number from 1-" + str(len(results['items'])) + ": ")

playlist_to_shuffle = int(playlist_to_shuffle)

songIDList = []
playlistURI = results['items'][playlist_to_shuffle-1]['uri']

# retrieve all tracks in the playlist
playlistContents = spotify.playlist_items(playlistURI)
for song in playlistContents['items']:
    songIDList.append(song['track']['id'])

# shuffle the tracks and save it
random.shuffle(songIDList)

spotify.playlist_replace_items(playlistURI, songIDList)

print("Shuffled the \"" + results['items'][playlist_to_shuffle-1]['name'] + "\" playlist.")