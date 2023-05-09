from playlistdownloader.downloader import PlaylistDownloader


class DownloaderService:
    def __init__(self, spotipy_id, spotipy_secret):
        self.PLD = PlaylistDownloader(
            spotipyid=spotipy_id, spotipysecret=spotipy_secret
        )

    def download_playlist(self, inputname, output_folder, compress):
        playlist = self.PLD.load_playlist(inputname)
        self.PLD.download_playlist(playlist, output_folder, compress=compress)
