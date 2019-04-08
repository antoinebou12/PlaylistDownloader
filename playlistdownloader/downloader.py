from __future__ import unicode_literals

from enum import Enum
from threading import Thread
import zipfile
import shutil
import re

from playlistdownloader.PlaylistFileStrategy import *


# File playlist enum
class TypePlaylist(Enum):
    OTHER = -1
    SONG_NAME = 0
    SOUNDCLOUD = 1
    YOUTUBE = 2
    SPOTIFY = 3


class PlaylistDownloader(object):

    def __init__(self, out="", playlist_type=TypePlaylist.YOUTUBE.value, spotipyid=None, spotipysecret=None):
        super(PlaylistDownloader, self).__init__()
        self._out = out

        self.spotipyid =spotipyid
        self.spotipysecret = spotipysecret

        self.__strategies = [SongNamePlaylistFile(), SoundCloudPlaylistFile(), YoutubePlaylistFile(), SpotifyPlaylistFile(spotipyid, spotipysecret)]
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

            try:
                if link_type == 3:
                    self.type_strategy.download_playlist(name, out)
                else:
                    print("(%d/%d) %s" % (i+1, len(playlist), name))
                    t = Thread(target=self.download_song, args=(name, out))
                    t.start()
                    t.join()
            except Exception:
                raise ("Thread Error")

        if compress:
            zipf = zipfile.ZipFile('{}.zip'.format(out), 'w', zipfile.ZIP_DEFLATED)
            PlaylistDownloader.zipdir(out, zipf)
            zipf.close()
            shutil.rmtree(out)

    def recognition_link(self, link):
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

    @staticmethod
    def zipdir(path, ziph):
        """
        https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
        """

        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))

    @property
    def type_strategy(self):
        return self._type_strategy

    @type_strategy.setter
    def type_strategy(self, index):
        self._type_strategy = self.__strategies[index]

    def change_strategy_link(self, link):
        link_type = self.recognition_link(link)
        if link_type == TypePlaylist.YOUTUBE.value:
            self._type_strategy = self.__strategies[TypePlaylist.YOUTUBE.value]
        elif link_type == TypePlaylist.SOUNDCLOUD.value:
            self._type_strategy = self.__strategies[TypePlaylist.SOUNDCLOUD.value]
        elif link_type == TypePlaylist.SPOTIFY.value:
            self._type_strategy = self.__strategies[TypePlaylist.SPOTIFY.value]
        elif link_type == TypePlaylist.SONG_NAME.value:
            self._type_strategy = self.__strategies[TypePlaylist.SONG_NAME.value]

        return link_type

