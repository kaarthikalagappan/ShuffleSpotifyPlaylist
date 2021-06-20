# Spotify Playlist Shuffler

## Why?

Google Home devices won't shuffle playlists when setting a media alarm.

Waking up to the same song every day will drive you nuts.

So here. Have a separate computer do the shuffling for you.

## Requirements
Run `pip3 install -r requirements.txt` to install all of dependencies required for this program.

Primary requirements:
 - A Spotify application in your developer account with a defined Redirect URI (it doesn't need to resolve). [Spotify Documentation](https://developer.spotify.com/documentation/general/guides/app-settings/)
    - Add `http://localhost:8080` to the Redirect URI Whitelist under the app settings
 - Python 3.x
 - [Spotipy](https://github.com/plamere/spotipy)

## Usage

In your config.cfg, enter in the appropriate fields:

- Your app's Client ID
- Client Secret 


On its first run, you will be prompted to log into your Spotify account in the browser and authorize the program to access to data. Upon successful authorization you'll be redirected to `http://localhost:8080` in your browser that will indicate the result of the operation. You can then close the tab.

An authorization token will be placed in the script's folder. No further interaction is needed and you won't be prompted to login in the future.

After authorization a list of all playlists owned by the user will be printed in the terminal. To shuffle a playlist, enter the number corresponding to that playlist in the printed list.