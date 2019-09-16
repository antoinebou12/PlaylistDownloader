import abc  # Python's built-in abstract class library

import os
import re
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

import spotipy
import spotipy.oauth2 as oauth2

import youtube_dl

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
    def __init__(self):
        super(SongNamePlaylistFile, self).__init__()
        self.loaded_playlist = None

    def load_playlist(self, fname, decode="\n"):
        """

        :param fname:
        :param decode:
        :return:
        """
        if os.path.isfile(fname) and not self.loaded_playlist is None:
            with open(fname) as fp:
                lines = fp.read().split(decode)  # Create a list containing all lines
            self.loaded_playlist = lines
        return self.loaded_playlist

    def download_song(self, link, out=".", quality=1):
        """
         TODO change this to a youtube-dl python function
         youtube-dl can do this also
        :param link:
        :param out:
        :param quality:
        :return:
        """
        try:
            os.subprocess.call(
                ["youtube-dl", "--extract-audio", "--audio-format", "mp3", "--audio-quality", str(quality), "-o",
                "{}/%(title)s.%(ext)s".format(out), link, "--no-playlist", "-i", "--default-search", "ytsearch", "-q", "--no-progress "])
        except Exception as e:
            ydl_opts = {
                'outtmpl': "{}/%(title)s.%(ext)s".format(out),
                'verbose': False,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])


class SoundCloudPlaylistFile(PlaylistFileStrategyAbstract):
    """
    Strategy used for soundcloud link
    """
    def __init__(self):
        super(SoundCloudPlaylistFile, self).__init__()
        self.loaded_playlist = None

    def load_playlist(self, fname, decode="\n"):
        """

        :param fname:
        :param decode:
        :return:
        """
        if os.path.isfile(fname) and not self.loaded_playlist is None:
            with open(fname) as fp:
                lines = fp.read().split(decode)  # Create a list containing all lines
            self.loaded_playlist = lines
        return self.loaded_playlist

    def download_song(self, link, out="."):
        """
        TODO change this to a scdl python function
        youtube-dl can do this also
        :param link:
        :param out:
        :return:
        """
        try:
            os.subprocess.call(["scdl", "-l", link, "--path", out, "--onlymp3", "-c", "--error", "--remove"])
        except Exception as e:
            try:
                os.subprocess.call(["youtube-dl", "--extract-audio", "--audio-format", "mp3", "-o",
                     "{}/%(title)s.%(ext)s".format(out), link, "--no-playlist", "-i", "--default-search", "ytsearch",
                     "-q", "--no-progress "])
            except Exception as e:
                ydl_opts = {
                    'outtmpl': "{}/%(title)s.%(ext)s".format(out),
                    'verbose': False,
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])


class YoutubePlaylistFile(PlaylistFileStrategyAbstract):
    """
    Strategy used for youtube link (normal video or playlist)
    """
    def __init__(self):
        super(YoutubePlaylistFile, self).__init__()
        self.loaded_playlist = None

    def load_playlist(self, fname, decode="\n"):
        """

        :param fname:
        :param decode:
        :return:
        """
        if os.path.isfile(fname) and not self.loaded_playlist:
            with open(fname) as fp:
                lines = fp.read().split(decode)  # Create a list containing all lines
            self.loaded_playlist = lines
        return self.loaded_playlist

    def download_song(self, link, out=".", quality=1):
        """
        # TODO fix error or use the console method or put subprocess
        :param link:
        :param out:
        :param quality:
        :return:
        """
        try:
            os.subprocess.call(
                ["youtube-dl", "--extract-audio", "--audio-format", "mp3", "--audio-quality", str(quality), "-o",
                "{}/%(title)s.%(ext)s".format(out), link, "-i", "-q", "--no-progress "])
        except Exception as e:

            ydl_opts = {
                'outtmpl': "{}/%(title)s.%(ext)s".format(out),
                'verbose': False,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])


    @staticmethod
    def write_youtube_playlist(url, out):
        """

        :param url:
        :param out:
        :return:
        """
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page.read(), "html.parser")
        href_tags = soup.find_all('a', {'class': 'pl-video-title-link'}, href=True)

        with open(out, 'w') as f:
            for i in href_tags:
                f.write("%s%s\n" % ("https://www.youtube.com", i['href']))
        f.close()

    @staticmethod
    def clean_y_dl():
        """
        TODO remove this method
        :return:
        """
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

        self.loaded_playlist = None

        self.spotipyid = spotipyid
        self.spotipysecret = spotipysecret

    @staticmethod
    def login_spotipy(client_id, client_secret):
        """

        :param client_id:
        :param client_secret:
        :return:
        """
        credentials = oauth2.SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )

        token = credentials.get_access_token()
        sp = spotipy.Spotify(auth=token)
        return sp

    def load_playlist(self, playlist, spotipyid=None, spotipysecret=None):
        """

        :param playlist:
        :param spotipyid:
        :param spotipysecret:
        :return:
        """
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
        """

        :param playlist:
        :param spotipy:
        :return:
        """
        if spotipy is None:
            spotipy = self.login_spotipy(self.spotipyid, self.spotipysecret)

        username = self.get_username_id(playlist)
        playlist_id = self.get_playlist_id(playlist)

        print(username, spotipy.user_playlist(username, playlist_id)['name'])

        tracks = self.tracks_playlist(spotipy, username, playlist_id)
        return tracks

    def load_playlist_file(self, playlist, spotipy=None):
        """

        :param playlist:
        :param spotipy:
        :return:
        """
        if spotipy is None:
            spotipy = self.login_spotipy(self.spotipyid, self.spotipysecret)

        all_tracks = []

        if os.path.isfile(playlist) and not self.loaded_playlist:
            with open(playlist) as fp:
                lines = fp.read().split("\n")  # Create a list containing all lines
                for link in lines:
                    username = self.get_username_id(link)
                    playlist_id = self.get_playlist_id(link)
                    print(username, spotipy.user_playlist(username, playlist_id)['name'])

                    tracks = self.tracks_playlist(spotipy, username, playlist_id)
                    for track in tracks:
                        all_tracks.append(track)
                    self.loaded_playlist = all_tracks
        return self.loaded_playlist

    @staticmethod
    def tracks_playlist(sp, username, playlist_id):
        """

        :param sp:
        :param username:
        :param playlist_id:
        :return:
        """
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
        """

        :param name:
        :param out:
        :param quality:
        :return:
        """
        try:
            os.subprocess.call(
                ["youtube-dl", "--extract-audio", "--audio-format", "mp3", "--audio-quality", str(quality), "-o",
                "{}/%(title)s.%(ext)s".format(out), name, "--no-playlist", "-i", "--default-search", "ytsearch", "-q", "--no-progress "])
        except Exception as e:

            ydl_opts = {
                'outtmpl': "{}/%(title)s.%(ext)s".format(out),
                'verbose': False,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([name])

    def download_playlist(self, name, out=".", quality=5):
        """

        :param name:
        :param out:
        :param quality:
        :return:
        """
        if not os.path.exists(str(out)):
            os.mkdir(str(out))

        playlist = self.load_playlist(name)

        for i, name in enumerate(playlist):
            with ThreadPoolExecutor() as executor:
                exe_results = [executor.submit(self.download_song, name, out, quality)]
                for exe in as_completed(exe_results):
                    try:
                        data = exe.result()
                    except Exception as e:
                        data = exe.result()
                        print(data)
                    print("     (%d/%d) %s" % (i + 1, len(playlist), name))

    @staticmethod
    def get_username_id(link):
        """
        http://www.txt2re.com
        :param link:
        :return:
        """
        regex_id = '.*?(?:[a-z][a-z]+).*?(?:[a-z][a-z]+).*?(?:[a-z][a-z]+).*?(?:[a-z][a-z]+).*?(?:[a-z][a-z]+).*?((?:[a-z][a-z]+))'
        rg = re.compile(regex_id,re.IGNORECASE | re.DOTALL)
        result = rg.search(link)
        if result:
            return result.group(1)
        else:
            return ''

    @staticmethod
    def get_playlist_id(link):
        """
        http://www.txt2re.com
        :param link:
        :return:
        """
        regex_id = '.*?(\\d+)((?:[a-z][a-z]*[0-9]+[a-z0-9]*))'  # Non-greedy match on filler

        rg = re.compile(regex_id, re.IGNORECASE | re.DOTALL)
        result = rg.search(link)
        if result:
            return result.group(1) + result.group(2)
        else:
            return -1

