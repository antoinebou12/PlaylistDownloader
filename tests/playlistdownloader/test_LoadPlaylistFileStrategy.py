import os

import pytest

from playlistdownloader.downloader import SoundCloudPlaylistFile
from playlistdownloader.downloader import SpotifyPlaylistFile
from playlistdownloader.downloader import YoutubePlaylistFile


class UtilsFunc:
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
        return list(os.listdir(dirname))


@pytest.fixture
def soundcloud():
    return SoundCloudPlaylistFile()


@pytest.fixture
def youtube():
    return YoutubePlaylistFile()


@pytest.fixture
def spotify():
    return SpotifyPlaylistFile()


class TestSoundCloudPlaylistFile:
    def test_load_playlist(self, soundcloud):
        load_playlist = soundcloud.load_playlist(
            f"{os.getcwd()}/tests/data/soundcloud-list.txt"
        )
        assert set(load_playlist) == set(
            UtilsFunc.read_file_to_list(f"{os.getcwd()}/tests/data/soundcloud-list.txt")
        )

    def test_load_playlist_FileNotFoundError(self, soundcloud):
        with pytest.raises(FileNotFoundError):
            soundcloud.load_playlist(f"{os.getcwd()}tests/data/no.txt")

    def test_download_song(self, soundcloud, tmpdir):
        load_playlist = soundcloud.load_playlist(
            f"{os.getcwd()}/tests/data/soundcloud-list.txt"
        )
        soundcloud.download_song(load_playlist[0], tmpdir)
        assert UtilsFunc.list_fname_dir(tmpdir)[0] == "L O N G    B E A C H.mp3"


class TestYoutubePlaylistFile:
    def test_load_playlist(self, youtube):
        load_playlist = youtube.load_playlist(
            f"{os.getcwd()}/tests/data/youtube-playlist.txt"
        )
        assert set(load_playlist) == set(
            UtilsFunc.read_file_to_list(
                f"{os.getcwd()}/tests/data/youtube-playlist.txt"
            )
        )

    def test_load_playlist_FileNotFoundError(self, youtube):
        with pytest.raises(FileNotFoundError):
            youtube.load_playlist(f"{os.getcwd()}tests/data/no.txt")

    def test_download_song(self, youtube, tmpdir):
        load_playlist = youtube.load_playlist(
            f"{os.getcwd()}/tests/data/youtube-playlist.txt"
        )
        youtube.download_song(load_playlist[0], tmpdir)
        assert UtilsFunc.list_fname_dir(tmpdir)[0] == "Darude - Sandstorm.mp3"


class TestSpotifyPlaylistFile:
    def test_login_spotipy(self, spotify):
        assert True

    def test_load_playlist(self, spotify):
        assert True

    def test_tracks_playlist(self, spotify):
        assert True

    def test_download_song(self, spotify):
        assert True
