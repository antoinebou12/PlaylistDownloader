import shutil
import tempfile
from unittest import TestCase

from playlistdownloader.downloader import PlaylistDownloader
from playlistdownloader.downloader import TypePlaylist


class TestPlaylistDownloader(TestCase):
    def setUp(self):
        self.playlistdownloader = PlaylistDownloader()
        self.soundcloud = PlaylistDownloader(
            playlist_type=TypePlaylist.SOUNDCLOUD.value
        )
        self.youtube = PlaylistDownloader(playlist_type=TypePlaylist.YOUTUBE.value)
        self.spotify = PlaylistDownloader(playlist_type=TypePlaylist.SPOTIFY.value)
        self.dirpath = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dirpath)

    # TODO write required test
    def test_load_playlist(self):
        assert True

    def test_download_song(self):
        assert True

    def test_download_playlist(self):
        assert True
