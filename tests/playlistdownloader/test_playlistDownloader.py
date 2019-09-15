from unittest import TestCase
import tempfile

from playlistdownloader.downloader import PlaylistDownloader, TypePlaylist


class TestPlaylistDownloader(TestCase):

    def setUp(self):
        self.playlistdownloader = PlaylistDownloader()
        self.soundcloud = PlaylistDownloader(playlist_type=TypePlaylist.YOUTUBE.value)
        self.youtube = PlaylistDownloader(playlist_type=TypePlaylist.YOUTUBE.value)
        self.spotify = PlaylistDownloader(playlist_type=TypePlaylist.YOUTUBE.value)
        self.dirpath = tempfile.mkdtemp()

    # TODO write required test
    def test_load_playlist(self):
        assert True

    def test_download_song(self):
        assert True

    def test_download_playlist(self):
        assert True
