from __future__ import unicode_literals

import shutil
import zipfile
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

from playlistdownloader.PlaylistFileStrategy import *
from playlistdownloader.constants import TypePlaylist


class PlaylistDownloader(object):
    def __init__(self, out="", playlist_type=TypePlaylist.YOUTUBE.value, spotipyid=None, spotipysecret=None):
        super(PlaylistDownloader, self).__init__()
        # output file
        self._out = out

        # Spotify
        self.spotipyid = spotipyid
        self.spotipysecret = spotipysecret

        self.__strategies = {
            'song_name': SongNamePlaylistFile(),
            'soundcloud':   SoundCloudPlaylistFile(),
            'youtube': YoutubePlaylistFile(),
            'spotify': SpotifyPlaylistFile(spotipyid, spotipysecret)
        }
        self._type_strategy = self.__strategies[playlist_type]

    # The playlist is a list of link or song name contain in a txt
    def load_playlist(self, *args, **kwargs):
        return self.type_strategy.load_playlist(*args, **kwargs)

    def download_song(self, *args, **kwargs):
        # self.change_strategy_link(args[0])
        return self.type_strategy.download_song(*args, **kwargs)

    def download_playlist(self, playlist, out="output", compress=False):
        if not os.path.exists(str(out)):
            os.mkdir(out)

        for i, name in enumerate(playlist):
            link_type = self.change_strategy_link(name)

            if link_type == 3:
                self.type_strategy.download_playlist(name, out)
            else:
                with ThreadPoolExecutor() as executor:
                    exe_results = [executor.submit(self.download_song, name, out)]

                    for result in as_completed(exe_results):
                        print("(%d/%d) %s" % (i + 1, len(playlist), name))

        if compress:
            zipf = zipfile.ZipFile('{}.zip'.format(out), 'w', zipfile.ZIP_DEFLATED)
            PlaylistDownloader.zipdir(out, zipf)
            zipf.close()
            shutil.rmtree(out)

    @staticmethod
    def recognition_link(link):
        main_url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', link)
        if not main_url:
            return TypePlaylist.SONG_NAME.value
        elif main_url[0] == 'https://soundcloud.com':
            return TypePlaylist.SOUNDCLOUD.value
        elif main_url[0] == 'https://www.youtube.com':
            if re.findall('(?<![\w\d])watch(?![\w\d])', link):
                return TypePlaylist.YOUTUBE.value
            elif re.findall('(?<![\w\d])playlist(?![\w\d])', link):
                return TypePlaylist.YOUTUBE.value
        elif main_url[0] == 'https://open.spotify.com':
            return TypePlaylist.SPOTIFY.value
        else:
            return TypePlaylist.OTHER.value

    @property
    def type_strategy(self):
        return self._type_strategy

    @type_strategy.setter
    def type_strategy(self, index):
        self._type_strategy = self.__strategies[index]

    def change_strategy_link(self, link):
        link_type = self.recognition_link(link)
        self._type_strategy = self.__strategies[TypePlaylist.YOUTUBE.value]

        return link_type

