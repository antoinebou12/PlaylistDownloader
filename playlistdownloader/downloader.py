from __future__ import unicode_literals

import os
import shutil
import zipfile
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

from playlistdownloader import recognition_link, TypePlaylist, SongNamePlaylistFile, SoundCloudPlaylistFile, \
    YoutubePlaylistFile, SpotifyPlaylistFile, zipdir


class PlaylistDownloader(object):
    def __init__(self, out="", playlist_type=TypePlaylist.YOUTUBE.value, spotipyid=None, spotipysecret=None):
        super(PlaylistDownloader, self).__init__()
        # output file
        self._out = out

        # Spotify
        self.spotipyid = spotipyid
        self.spotipysecret = spotipysecret

        self.__strategies = {
            0: SongNamePlaylistFile(),
            1: SoundCloudPlaylistFile(),
            2: YoutubePlaylistFile(),
            3: SpotifyPlaylistFile(spotipyid, spotipysecret)
        }
        self._type_strategy = self.__strategies.get(playlist_type, SongNamePlaylistFile())

    def load_playlist(self, *args, **kwargs):
        """
        The playlist is a list of link or song name contain in a txt
        :param args:
        :param kwargs:
        :return:
        """
        return self.type_strategy.load_playlist(*args, **kwargs)

    def download_song(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        return self.type_strategy.download_song(*args, **kwargs)

    def download_playlist(self, playlist, out="output", compress=False):
        """

        :param playlist:
        :param out:
        :param compress:
        :return:
        """
        if not os.path.exists(str(out)):
            os.mkdir(out)

        for i, name in enumerate(playlist):
            if name:
                link_type = self.change_strategy_link(name)

                if link_type == 3:
                    self.type_strategy.download_playlist(name, out)
                else:
                    with ThreadPoolExecutor(max_workers=10) as executor:
                        exe_results = [executor.submit(self.download_song, name, out)]

                        for exe in as_completed(exe_results):
                            try:
                                data = exe.result()
                            except Exception as e:
                                data = exe.result()
                                print(data)
                            print("({}/{}) {}".format(i + 1, len(playlist), name))

        if compress:
            zipf = zipfile.ZipFile('{}.zip'.format(out), 'w', zipfile.ZIP_DEFLATED)
            zipdir(out, zipf)
            zipf.close()
            shutil.rmtree(out)

    @property
    def type_strategy(self):
        """

        :return:
        """
        return self._type_strategy

    @type_strategy.setter
    def type_strategy(self, index):
        """

        :param index:
        :return:
        """
        self._type_strategy = self.__strategies[index]

    def change_strategy_link(self, link):
        """

        :param link:
        :return:
        """
        link_type = recognition_link(link)
        self._type_strategy = self.__strategies.get(link_type, SongNamePlaylistFile())

        return link_type

