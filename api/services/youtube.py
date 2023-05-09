from playlist_downloader.downloader import PlaylistDownloader
from playlist_downloader.downloader import TypePlaylist


class YoutubeService:
    def __init__(self):
        self.PLD_youtube = PlaylistDownloader(playlist_type=TypePlaylist.YOUTUBE.value)

    def download_playlist(self, inputname, output_folder, compress):
        youtube_list = self.PLD_youtube.load_playlist(inputname)
        self.PLD_youtube.download_playlist(
            youtube_list, output_folder, compress=compress
        )
