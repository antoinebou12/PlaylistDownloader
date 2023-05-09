from playlist_downloader.downloader import PlaylistDownloader
from playlist_downloader.downloader import TypePlaylist


class SoundCloudService:
    def __init__(self):
        self.PLD_soundcloud = PlaylistDownloader(
            "soundcloud", playlist_type=TypePlaylist.SOUNDCLOUD.value
        )

    def download_playlist(self, inputname, output_folder, compress):
        soundcloud_list = self.PLD_soundcloud.load_playlist(inputname)
        self.PLD_soundcloud.download_playlist(
            soundcloud_list, output_folder, compress=compress
        )
