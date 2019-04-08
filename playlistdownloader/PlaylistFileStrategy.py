import abc  # Python's built-in abstract class library

import os
import subprocess
import re
from threading import Thread

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
        :param args:
        :param kwargs:
        """

    @abc.abstractmethod
    def download_song(self, *args, **kwargs):
        """Required Method
        :param args:
        :param kwargs:
        """


# SoundCloud strategy
class SongNamePlaylistFile(PlaylistFileStrategyAbstract):

    def load_playlist(self, fname, decode="\n"):
        if os.path.isfile(fname):
            with open(fname) as fp:
                lines = fp.read().split(decode)  # Create a list containing all lines
            return lines
        else:
            raise FileNotFoundError("Wrong path or the file doesn't exist")

    # youtube-dl can do this also
    def download_song(self, link, out=".", quality=1):

        subprocess.call(["youtube-dl", "--extract-audio", "--audio-format", "mp3", "--audio-quality", str(quality), "-o", "{}/%(title)s.%(ext)s".format(out), link, "--no-playlist", "-i", "--default-search", "ytsearch", "-q"])


# SoundCloud strategy
class SoundCloudPlaylistFile(PlaylistFileStrategyAbstract):

    def load_playlist(self, fname, decode="\n"):
        if os.path.isfile(fname):
            with open(fname) as fp:
                lines = fp.read().split(decode)  # Create a list containing all lines
            return lines
        else:
            raise FileNotFoundError("Wrong path or the file doesn't exist")

    # youtube-dl can do this also
    def download_song(self, link, out="."):

        subprocess.call(["scdl", "-l", link, "--path", out, "--onlymp3", "-c", "--error"])

        # if not os.path.exists(str(os.path.basename(out))):
        #     os.mkdir(str(os.path.basename(out)))
        #
        # subprocess.call(["youtube-dl", "--extract-audio", "--audio-format", "mp3", "--audio-quality", str(quality), "-o", "{}/%(title)s.%(ext)s".format(out), name, "--yes-playlist", "-i"])


# Youtube strategy
class YoutubePlaylistFile(PlaylistFileStrategyAbstract):

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


# Spotify strategy
class SpotifyPlaylistFile(PlaylistFileStrategyAbstract):

    def __init__(self, spotipyid=None, spotipysecret=None) -> None:
        super(SpotifyPlaylistFile).__init__()

        self.spotipyid = spotipyid
        self.spotipysecret = spotipysecret

    def load_playlist(self, playlist, spotipyid=None, spotipysecret=None):
        if spotipyid is None:
            spotipyid = self.spotipyid
        if spotipysecret is None:
            spotipysecret = self.spotipysecret

        spotipy = self.login_spotipy(self.spotipyid, self.spotipysecret)

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
    def login_spotipy(client_id, client_secret):
            credentials = oauth2.SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )

            token = credentials.get_access_token()
            sp = spotipy.Spotify(auth=token)
            return sp

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
            try:
                print("     (%d/%d) %s" % (i+1, len(playlist), name))
                t = Thread(target=self.download_song, args=(name, out, quality))
                t.start()
                t.join()
            except Exception:
                raise ("Thread Error")


    @staticmethod
    def get_username_id(link):
        # http://www.txt2re.com
        re1 = '.*?'  # Non-greedy match on filler
        re2 = '(?:[a-z][a-z]+)'  # Uninteresting: word
        re3 = '.*?'  # Non-greedy match on filler
        re4 = '(?:[a-z][a-z]+)'  # Uninteresting: word
        re5 = '.*?'  # Non-greedy match on filler
        re6 = '(?:[a-z][a-z]+)'  # Uninteresting: word
        re7 = '.*?'  # Non-greedy match on filler
        re8 = '(?:[a-z][a-z]+)'  # Uninteresting: word
        re9 = '.*?'  # Non-greedy match on filler
        re10 = '(?:[a-z][a-z]+)'  # Uninteresting: word
        re11 = '.*?'  # Non-greedy match on filler
        re12 = '((?:[a-z][a-z]+))'  # Word 1

        rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8 + re9 + re10 + re11 + re12,
                        re.IGNORECASE | re.DOTALL)
        m = rg.search(link)
        if m:
            word = m.group(1)
            return word

    @staticmethod
    def get_playlist_id(link):
        # http://www.txt2re.com
        re1 = '.*?'  # Non-greedy match on filler
        re2 = '(\\d+)'  # Integer Number 1
        re3 = '((?:[a-z][a-z]*[0-9]+[a-z0-9]*))'  # Alphanum 1

        rg = re.compile(re1 + re2 + re3, re.IGNORECASE | re.DOTALL)
        m = rg.search(link)
        if m:
            int = m.group(1)
            alphanum = m.group(2)
            return int + alphanum