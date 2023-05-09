"""
This script is a command-line tool for downloading playlists from various sources like Spotify, YouTube, SoundCloud, or even from a text file containing song names.
It uses the strategy pattern to define different strategies for loading and downloading playlists from various sources
"""
import abc  # Python's built-in abstract class library
import os
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

from playlistdownloader.playlist.Song import SongNamePlaylistFile


# Strategy Pattern
class PlaylistStrategyAbstract:

    """You do not need to know about metaclasses.
    Just know that this is how you define abstract
    classes in Python."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def load_playlist(self, *args, **kwargs):
        """Required Method
        :param args: args based on the specific strategy
        :param kwargs: kwargs based on the specific strategy
        """

    @abc.abstractmethod
    def download_song(self, *args, **kwargs):
        """Required Method
        :param args: args based on the specific strategy
        :param kwargs: kwargs based on the specific strategy
        """


class MusicDownloader:
    def __init__(self, strategy):
        self.strategy = strategy

    def load_playlist(self, *args, **kwargs):
        return self.strategy.load_playlist(*args, **kwargs)

    def download_song(self, *args, **kwargs):
        return self.strategy.download_song(*args, **kwargs)

    def download_all(self, out_dir=".", quality=1, max_workers=5):
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.download_song, song, out_dir, quality)
                for song in self.strategy.loaded_playlist
            ]

            for future in as_completed(futures):
                future.result()


if __name__ == "__main__":
    text_file_downloader = MusicDownloader(SongNamePlaylistFile())
    text_file_downloader.load_playlist("song_list.txt")
    text_file_downloader.download_all(
        out_dir="downloaded_music", quality=1, max_workers=5
    )
