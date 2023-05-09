import shutil
import tempfile
from unittest import TestCase

from playlist_downloader.downloader import PlaylistDownloader
from playlist_downloader.downloader import TypePlaylist


class TestPlaylistDownloader(TestCase):
    """Test PlaylistDownloader"""

    def setUp(self):
        """Create temporary directory"""
        self.playlistdownloader = PlaylistDownloader()
        self.soundcloud = PlaylistDownloader(
            playlist_type=TypePlaylist.SOUNDCLOUD.value
        )
        self.youtube = PlaylistDownloader(playlist_type=TypePlaylist.YOUTUBE.value)
        self.spotify = PlaylistDownloader(playlist_type=TypePlaylist.SPOTIFY.value)
        self.dirpath = tempfile.mkdtemp()

    def tearDown(self):
        """Delete temporary directory and all its contents"""
        shutil.rmtree(self.dirpath)

    # TODO write required test
    def test_load_playlist(self):
        """Test load playlist"""
        assert True

    def test_download_song(self):
        """Test download song"""
        assert True

    def test_download_playlist(self):
        """Test download playlist"""
        assert True
