# PlaylistDownloader
This is a project to download mp3 file (song, etc) for multiple provider with a easy python extension of existing library, but this project extends on this
- downloader that auto detect the provider of the audio file required
- with a rest-api that parse list of playlist or song in a text file

[youtube-dl](https://github.com/ytdl-org/youtube-dl) got pretty much all those feature. this program is basically a wrapper to youtube-dl

Download a playlist (spotify, youtube) by finding  download the mp3 of the music video youtube

## Install
_For now the Windows is not that well supported_

Install all require package
```bash
python3 setup.py install --user
```

Ubuntu and WSL
Fix bug with youtube search with youtube-dl
```bash
./scripts/youtube-dl.sh
```
Fix bug with youtube-dl download
```bash
sudo apt-get install ffmpeg
```

Change the api key for spotify with your own key [Spotify Developer App](https://developer.spotify.com/dashboard/login) to make it work in 

- `rest/rest.py`
- `examples/random_link.py`
- `examples/spotify_link.py`

```python
# Spotipy Client ID
SPOTIPYCLIENTID = "SPOTIPY_CLIENT_ID"
SPOTIPYCLIENTSECRET = "SPOTIPY_CLIENT_ID"
```

### TODO

- [] no API key for spotify
- [] add more provider


## How To Use
Work with different music platform like 
- soundcloud, 
- youtube
- spotify(require api key)

### Auto-recognition of link
Download a playlists containing link for the 3 different services

```bash  
python3 random-playlink.py data/random-list.txt --output random
```

### Youtube

Download a list of link of youtube video
```bash  
python3 youtube-playlist.py data/youtube-list.txt --output youtube
```

### SoundCloud

Download a list of link of soundcloud
```bash  
python3 soundcloud-playlist.py data/soundcloud-list.txt --output soundcloud
```

### Spotify

Download a playlist of spotify
```bash  
python3 spotify-playlist.py "https://open.spotify.com/user/spotifycharts/playlist/37i9dQZEVXbMDoHDwVN2tF?si=ZBG2E3XeSbGHEH0vZcYYTQ"  --output "Spotify-Playlist"
```
Download a playlist of spotify with special api key
```bash  
python3 spotify-playlist.py "https://open.spotify.com/user/spotifycharts/playlist/37i9dQZEVXbMDoHDwVN2tF?si=ZBG2E3XeSbGHEH0vZcYYTQ" --output "Spotify-Playlist" --spotipyid CLIENTID --spotipysecret CLIENTSECRET"
```
Get Spotify link for the playlist id and username
![Get Spotify link for the playlist id](image/spotify_uri.jpg "Spotify URI GET")

## Rest API
### TODO

- [] Change the rest api to not save data locally on the server
- [] Cleaner simpler UI
- [] Simpler installation and setup
- [] 
- [] Add more provider
### Start server

 ```bash  
python3 rest.py
```

### Test the API with curl
 ```bash  
curl -X POST http://127.0.0.1:5000/api/downloader/random-list.txt
curl -X GET http://127.0.0.1:5000/api/playlist/download_0.zip
```

###  Test the API with web interface
 ```bash  
python3 rest.py
```

open that`\rest\index.html` or `http://127.0.0.1:5000/index.html` in a browser
- choose file
- read file
- save new file
- chose new file
- Upload file
- Download playlist


### REST API INFO
routing for the web rest API

- Soundcloud:  `/api/soundcloud/<file>` GET
- Youtube:  `/api/youtube/<file>` GET
- Spotify:  `/api/spotify/<link>` or `/api/spotify/<file>` GET
- Downloader:  `/api/downloader/<file>` GET
- Download `/api/playlist/<item>` GET
- View List `/api/view/<item>` GET
- Upload list`/api/upload` POST

