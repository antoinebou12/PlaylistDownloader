# PlaylistDownloader

PlaylistDownloader is a project to download audio files (songs, etc.) from multiple providers with a simple Python extension of existing libraries. The project extends the following features:

- Auto-detects the provider of the required audio file
- Provides a REST API that parses a list of playlists or songs in a text file

This program is essentially a wrapper for [youtube-dl](https://github.com/ytdl-org/youtube-dl), which already offers most of these features.

PlaylistDownloader downloads playlists (from Spotify, YouTube, etc.) by finding and downloading the MP3 files of the music videos on YouTube.

## Installation

_For now, Windows is not well supported._

Install all required packages:

```bash
pip install poetry
poetry install
```

### Ubuntu and WSL

Fix bug with YouTube search using youtube-dl:

```bash
./scripts/youtube-dl.sh
```

Fix bug with youtube-dl download:

```bash
sudo apt-get install ffmpeg
```

Change the API key for Spotify with your own key [Spotify Developer App](https://developer.spotify.com/dashboard/login) to make it work in:

- `rest/rest.py`
- `examples/random_link.py`
- `examples/spotify_link.py`

```python
# Spotipy Client ID
SPOTIPYCLIENTID = "SPOTIPY_CLIENT_ID"
SPOTIPYCLIENTSECRET = "SPOTIPY_CLIENT_ID"
```

### TODO

- [ ] No API key for Spotify
- [ ] Add more providers

## How To Use

PlaylistDownloader works with different music platforms like:

- SoundCloud
- YouTube
- Spotify (requires API key)

### Auto-recognition of links

Download playlists containing links for the three different services:

```bash
python3 random-playlink.py data/random-list.txt --output random
```

### YouTube

Download a list of YouTube video links:

```bash
python3 youtube-playlist.py data/youtube-list.txt --output youtube
```

### SoundCloud

Download a list of SoundCloud links:

```bash
python3 soundcloud-playlist.py data/soundcloud-list.txt --output soundcloud
```

### Spotify

Download a Spotify playlist:

```bash
python3 spotify-playlist.py "https://open.spotify.com/user/spotifycharts/playlist/37i9dQZEVXbMDoHDwVN2tF?si=ZBG2E3XeSbGHEH0vZcYYTQ"  --output "Spotify-Playlist"
```

Download a Spotify playlist with a specific API key:

```bash
python3 spotify-playlist.py "https://open.spotify.com/user/spotifycharts/playlist/37i9dQZEVXbMDoHDwVN2tF?si=ZBG2E3XeSbGHEH0vZcYYTQ" --output "Spotify-Playlist" --spotipyid CLIENTID --spotipysecret CLIENTSECRET"
```

Get the Spotify link for the playlist ID and username:

![Get Spotify link for the playlist id](image/spotify_uri.jpg "Spotify URI GET")

## REST API

### TODO

- [ ] Change the REST API to not save data locally on the server
- [ ] Create a cleaner, simpler UI
- [ ] Simplify installation and setup
- [ ] Add more providers

### Start server

```bash
python3 rest.py
```

### Test the API with curl

```bash
curl -X POST http://127.0.0.1:5000/api/downloader/random-list.txt
curl -X GET http://127.0.0.1:5000/api
