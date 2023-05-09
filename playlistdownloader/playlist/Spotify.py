from asyncio import as_completed
from concurrent.futures import ThreadPoolExecutor

import youtube_dl

from playlistdownloader.playlist.PlaylistStrategy import PlaylistStrategyAbstract


class SpotifyPlaylistFile(PlaylistStrategyAbstract):
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
        return spotipy.Spotify(auth=token)

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

        return self.tracks_playlist(spotipy, username, playlist_id)

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
                    all_tracks.extend(iter(tracks))
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
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        return [
            f"{str(track['track']['artists'][0]['name'])} {str(track['track']['name'])}"
            for track in tracks
        ]

    def download_song(self, name, out=".", quality=5):
        """

        :param name:
        :param out:
        :param quality:
        :return:
        """
        try:
            os.subprocess.call(
                [
                    "youtube-dl",
                    "--extract-audio",
                    "--audio-format",
                    "mp3",
                    "--audio-quality",
                    str(quality),
                    "-o",
                    f"{out}/%(title)s.%(ext)s",
                    name,
                    "--no-playlist",
                    "-i",
                    "--default-search",
                    "ytsearch",
                    "-q",
                    "--no-progress ",
                ]
            )
        except Exception as e:

            ydl_opts = {
                'outtmpl': f"{out}/%(title)s.%(ext)s",
                'verbose': False,
                'format': 'bestaudio/best',
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }
                ],
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
        return result.group(1) if (result := rg.search(link)) else ''

    @staticmethod
    def get_playlist_id(link):
        """
        http://www.txt2re.com
        :param link:
        :return:
        """
        regex_id = '.*?(\\d+)((?:[a-z][a-z]*[0-9]+[a-z0-9]*))'  # Non-greedy match on filler

        rg = re.compile(regex_id, re.IGNORECASE | re.DOTALL)
        return result.group(1) + result.group(2) if (result := rg.search(link)) else -1

