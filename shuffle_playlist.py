import random
import spotipy
from os import path, system
import configparser
from datetime import datetime


def shufflePlaylist(playlistURI, spotify_client = None):
    scriptPath = path.dirname(path.realpath(__file__))
    
    # date and time when this is triggered
    date_time_now = datetime.now()

    # if already created spotify client is passed, then check if
    # the authorization cache exists
    if spotify_client == None:
        # getting the default cache path (from spotshuffle)
        cachePath = scriptPath+'/spotifytokencache'

        scope = 'user-library-read playlist-modify-public playlist-modify-private'

        config = configparser.ConfigParser()
        config.read(scriptPath+'/config.cfg')

        # making sure authorization token is present to avoid making user login
        if not path.isfile(cachePath):
            system("echo \"" + date_time_now.strftime("%d/%m/%Y %H:%M:%S") + 
                   ": Cached authorization token not found, please run spotshuffle program first.\"" + 
                   " >> " + scriptPath + "/log.txt")
            # print("Cached authorization token not found, please run spotshuffle program first.")
            exit(1)

        # Tries to authorize the user with cached token
        try:
            spotify_client = spotipy.Spotify(
                auth_manager=spotipy.oauth2.SpotifyOAuth(
                    client_id=config.get('APPDATA', 'CLIENT_ID'),
                    client_secret=config.get('APPDATA', 'CLIENT_SECRET'),
                    redirect_uri=config.get('APPDATA', 'REDIRECT_URI'),
                    scope=scope,
                    cache_path=cachePath,
                    open_browser=False
                )
            )
        except spotipy.oauth2.SpotifyOauthError:
            system("echo \"" + date_time_now.strftime("%d/%m/%Y %H:%M:%S") + 
                   ": Unable to obtain Spotify permissions with cached token.\"" + 
                   " >> " + scriptPath + "/log.txt")
            # print("Unable to obtain Spotify permissions with cached token")
            exit(1)

    songIDList = []

    # can only retrieve 100 tracks at once
    # so we loop 100 times (max playlist size is 10,000)
    for x in range(0, 10000, 100):
        # retrieve all tracks in the playlist from offset
        playlistContents = spotify_client.playlist_items(playlistURI, offset=x)
        if not playlistContents['items']:
            break
        for song in playlistContents['items']:
            songIDList.append(song['track']['id'])

    # shuffle the tracks and save it
    random.shuffle(songIDList)

    songIDLength = len(songIDList)

    # clear the playlist
    spotify_client.playlist_replace_items(playlistURI, [])

    # can only add 100 tracks at once
    # so we iterate till we have added all tracks
    for x in range(0, songIDLength, 100):
        spotify_client.user_playlist_add_tracks(spotify_client.me, playlistURI, songIDList[x:x+100], position=x)


if __name__ == "__main__":
    import sys
    shufflePlaylist(str(sys.argv[1]))