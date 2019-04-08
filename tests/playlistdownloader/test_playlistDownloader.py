from unittest import TestCase
import pytest

import os
import time
import tempfile
import shutil

from playlistdownloader.downloader import PlaylistDownloader, TypePlaylist


class TestPlaylistDownloader(TestCase):

    def setUp(self):
        self.soundcloud = PlaylistDownloader(playlist_type=TypePlaylist.YOUTUBE.value)
        self.youtube = PlaylistDownloader(playlist_type=TypePlaylist.YOUTUBE.value)
        self.spotify = PlaylistDownloader(playlist_type=TypePlaylist.YOUTUBE.value)
        self.dirpath = tempfile.mkdtemp()

    def test_load_playlist(self):
        assert True

    def test_download_song(self):
        assert True

    def test_download_playlist(self):
        assert True

    def test_write_playlist(self):
        assert True

    def test_zipdir(self):
        assert True