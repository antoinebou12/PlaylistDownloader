import abc  # Python's built-in abstract class library

import os
import subprocess
import re
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

import spotipy
import spotipy.oauth2 as oauth2

from bs4 import BeautifulSoup
import urllib


# Strategy Pattern
class PlaylistFileStrategyAbstract(object):

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


class SongNamePlaylistFile(PlaylistFileStrategyAbstract):
    """
    Strategy used when there no link only a song name
    """
    def load_playlist(self, fname, decode="\n"):
        if os.path.isfile(fname):
            with open(fname) as fp:
                lines = fp.read().split(decode)  # Create a list containing all lines
            return lines
        else:
            raise FileNotFoundError("Wrong path or the file doesn't exist")

    # youtube-dl can do this also
    def download_song(self, link, out=".", quality=1):
        # TODO change this to a youtube-dl python function
        subprocess.call(["youtube-dl", "--extract-audio", "--audio-format", "mp3", "--audio-quality", str(quality), "-o", "{}/%(title)s.%(ext)s".format(out), link, "--no-playlist", "-i", "--default-search", "ytsearch", "-q"])


class SoundCloudPlaylistFile(PlaylistFileStrategyAbstract):
    """
    Strategy used for soundcloud link
    """
    def load_playlist(self, fname, decode="\n"):
        if os.path.isfile(fname):
            with open(fname) as fp:
                lines = fp.read().split(decode)  # Create a list containing all lines
            return lines
        else:
            raise FileNotFoundError("Wrong path or the file doesn't exist")

    # youtube-dl can do this also
    def download_song(self, link, out="."):
        # TODO change this to a scdl python function
        subprocess.call(["scdl", "-l", link, "--path", out, "--onlymp3", "-c", "--error"])


class YoutubePlaylistFile(PlaylistFileStrategyAbstract):
    """
    Strategy used for youtube link (normal video or playlist)
    """
    def load_playlist(self, fname, decode="\n"):
        if os.path.isfile(fname):
            with open(fname) as fp:
                lines = fp.read().split(decode)  # Create a list containing all lines
            return lines
        else:
            raise FileNotFoundError("Wrong path or the file doesn't exist")

    # TODO fix error or use the console method or put subprocess
    def download_song(self, link, out=".", quality=1):
        subprocess.call(["youtube-dl", "--extract-audio", "--audio-format", "mp3", "--audio-quality", str(quality), "-o", "{}/%(title)s.%(ext)s".format(out), link, "-i", "-q"])

    @staticmethod
    def write_youtube_playlist(url, out):
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page.read(), "html.parser")
        href_tags = soup.find_all('a', {'class': 'pl-video-title-link'}, href=True)

        with open(out, 'w') as f:
            for i in href_tags:
                f.write("%s%s\n" % ("https://www.youtube.com", i['href']))
        f.close()

    @staticmethod
    def clean_y_dl():
        current = os.listdir('.')
        for file in current:
            if file.endswith(("mkv", "webm", ".part")):
                os.remove(file)


class SpotifyPlaylistFile(PlaylistFileStrategyAbstract):
    """
    Strategy used for spotify link (playlist)
    """

    def __init__(self, spotipyid=None, spotipysecret=None) -> None:
        super(SpotifyPlaylistFile).__init__()

        self.spotipyid = spotipyid
        self.spotipysecret = spotipysecret

    @staticmethod
    def login_spotipy(client_id, client_secret):
            credentials = oauth2.SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )

            token = credentials.get_access_token()
            sp = spotipy.Spotify(auth=token)
            return sp

    def load_playlist(self, playlist, spotipyid=None, spotipysecret=None):
        if spotipyid is None:
            spotipyid = self.spotipyid
        if spotipysecret is None:
            spotipysecret = self.spotipysecret

        spotipy = self.login_spotipy(spotipyid, spotipysecret)

        if os.path.isfile(str(playlist)):
            return self.load_playlist_file(playlist, spotipy=spotipy)
        else:
            return self.load_playlist_spotify(playlist, spotipy=spotipy)

    def load_playlist_spotify(self, playlist, spotipy=None):
        if spotipy is None:
            spotipy = self.login_spotipy(self.spotipyid, self.spotipysecret)

        username = self.get_username_id(playlist)
        playlist_id = self.get_playlist_id(playlist)

        print(username, spotipy.user_playlist(username, playlist_id)['name'])

        tracks = self.tracks_playlist(spotipy, username, playlist_id)
        return tracks

    def load_playlist_file(self, playlist, spotipy=None):
        if spotipy is None:
            spotipy = self.login_spotipy(self.spotipyid, self.spotipysecret)

        all_tracks = []

        if os.path.isfile(playlist):
            with open(playlist) as fp:
                lines = fp.read().split("\n")  # Create a list containing all lines
                for link in lines:
                    username = self.get_username_id(link)
                    playlist_id = self.get_playlist_id(link)
                    print(username, spotipy.user_playlist(username, playlist_id)['name'])

                    tracks = self.tracks_playlist(spotipy, username, playlist_id)
                    for track in tracks:
                        all_tracks.append(track)

                return all_tracks
        else:
            raise FileNotFoundError("Wrong path or the file doesn't exist")

    @staticmethod
    def tracks_playlist(sp, username, playlist_id):
        results = sp.user_playlist_tracks(username, playlist_id)
        tracks = results['items']
        songs_title = []
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        for track in tracks:
            songs_title.append("%s %s" % (str(track['track']['artists'][0]['name']), str(track['track']['name'])))
        return songs_title

    def download_song(self, name, out=".", quality=5):
        subprocess.call(
            ["youtube-dl", "--extract-audio", "--audio-format", "mp3", "--audio-quality", str(quality), "-o", "{}/%(title)s.%(ext)s".format(out), name, "--no-playlist", "-i", "--default-search", "ytsearch", "-q"])

    def download_playlist(self, name, out=".", quality=5):
        if not os.path.exists(str(out)):
            os.mkdir(str(out))

        playlist = self.load_playlist(name)

        for i, name in enumerate(playlist):
            with ThreadPoolExecutor() as executor:
                exe_results = [executor.submit(self.download_song, name, out, quality)]
                for result in as_completed(exe_results ):
                    print("     (%d/%d) %s" % (i + 1, len(playlist), name))

    @staticmethod
    def get_username_id(link):
        # http://www.txt2re.com
        regex_id = '.*?(?:[a-z][a-z]+).*?(?:[a-z][a-z]+).*?(?:[a-z][a-z]+).*?(?:[a-z][a-z]+).*?(?:[a-z][a-z]+).*?((?:[a-z][a-z]+))'
        rg = re.compile(regex_id,re.IGNORECASE | re.DOTALL)
        result = rg.search(link)
        if result:
            return result.group(1)
        else:
            return ''

    @staticmethod
    def get_playlist_id(link):
        # http://www.txt2re.com
        regex_id = '.*?(\\d+)((?:[a-z][a-z]*[0-9]+[a-z0-9]*))'  # Non-greedy match on filler

        rg = re.compile(regex_id, re.IGNORECASE | re.DOTALL)
        result = rg.search(link)
        if result:
            return result.group(1) + result.group(2)
        else:
            return -1
