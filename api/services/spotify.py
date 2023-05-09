from playlistdownloader.downloader import PlaylistDownloader
from playlistdownloader.downloader import TypePlaylist


class SpotifyService:
    def __init__(self, spotipy_id, spotipy_secret):
        self.PLD_spotify = PlaylistDownloader(
            playlist_type=TypePlaylist.SPOTIFY.value,
            spotipyid=spotipy_id,
            spotipysecret=spotipy_secret,
        )

    def download_playlist(self, inputname, output_folder, compress):
        spotify_list = self.PLD_spotify.load_playlist(inputname)
        self.PLD_spotify.download_playlist(
            spotify_list, output_folder, compress=compress
        )
