from unittest import TestCase
import pytest

import os
import time
import tempfile
import shutil

from playlistdownloader.downloader import SoundCloudPlaylistFile, YoutubePlaylistFile, SpotifyPlaylistFile


class UtilsFunc(object):

    @staticmethod
    def read_file_to_list(fname):
        if os.path.isfile(fname):
            with open(fname) as fp:
                lines = fp.read().split("\n")
            return lines
        else:
            raise FileNotFoundError("Wrong path or the file doesn't exist")

    @staticmethod
    def list_fname_dir(dirname):
        files = []
        for file in os.listdir(dirname):
            files.append(file)
        return files


class TestSoundCloudPlaylistFile(TestCase):

    def setUp(self):
        self.soundcloud = SoundCloudPlaylistFile()
        self.load_playlist = self.soundcloud.load_playlist(os.getcwd() + "/tests/data/soundcloud-list.txt")
        self.dirpath = tempfile.mkdtemp()

    def test_load_playlist(self):
        assert set(self.load_playlist) == set(UtilsFunc.read_file_to_list(os.getcwd() + "/tests/data/soundcloud-list.txt"))

    def test_load_playlist_FileNotFoundError(self):
        with pytest.raises(FileNotFoundError):
            self.soundcloud.load_playlist(os.getcwd() + "tests/data/no.txt")

    def test_download_song(self):

        self.soundcloud.download_song(self.load_playlist[0], self.dirpath)
        assert UtilsFunc.list_fname_dir(self.dirpath)[0] == "L O N G    B E A C H.mp3"

    def tearDown(self):
        shutil.rmtree(self.dirpath)


class TestYoutubePlaylistFile(TestCase):

    def setUp(self):
        self.youtube = YoutubePlaylistFile()
        self.load_playlist = self.youtube.load_playlist(os.getcwd() + "/tests/data/youtube-playlist.txt")
        self.dirpath = tempfile.mkdtemp()

    def test_load_playlist(self):
        assert set(self.load_playlist) == set(UtilsFunc.read_file_to_list(os.getcwd() + "/tests/data/youtube-playlist.txt"))

    def test_load_playlist_FileNotFoundError(self):
        with pytest.raises(FileNotFoundError):
            self.youtube.load_playlist(os.getcwd() + "tests/data/no.txt")

    def test_download_song(self):
        self.youtube.download_song(self.load_playlist[0], self.dirpath)
        assert UtilsFunc.list_fname_dir(self.dirpath)[0] == "Darude - Sandstorm.mp3"

    def tearDown(self):
        shutil.rmtree(self.dirpath)


# TODO Spotify
class TestSpotifyPlaylistFile(TestCase):

    def setUp(self):
        self.spotify = SpotifyPlaylistFile()

    def test_login_spotipy(self):
        assert True

    def test_load_playlist(self):
        assert True

    def test_tracks_playlist(self):
        assert True

    def test_download_song(self):
        assert True

    def tearDown(self):
        assert True


