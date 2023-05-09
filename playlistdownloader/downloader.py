from __future__ import unicode_literals
import os
import shutil
import zipfile
from concurrent.futures import as_completed, ThreadPoolExecutor
from pathlib import Path

from playlistdownloader import recognition_link, TypePlaylist, SongNamePlaylistFile, SoundCloudPlaylistFile, \
    YoutubePlaylistFile, SpotifyPlaylistFile, zipdir


class PlaylistDownloader:
    def __init__(self, out: str = "", playlist_type: int = TypePlaylist.YOUTUBE.value, spotipyid: str = None, spotipysecret: str = None):
        self._out = out
        self.spotipyid = spotipyid
        self.spotipysecret = spotipysecret

        strategies = {
            TypePlaylist.SONG_NAME.value: SongNamePlaylistFile(),
            TypePlaylist.SOUNDCLOUD.value: SoundCloudPlaylistFile(),
            TypePlaylist.YOUTUBE.value: YoutubePlaylistFile(),
            TypePlaylist.SPOTIFY.value: SpotifyPlaylistFile(spotipyid, spotipysecret)
        }

        self._type_strategy = strategies.get(playlist_type, SongNamePlaylistFile())

    def load_playlist(self, *args, **kwargs):
        return self.type_strategy.load_playlist(*args, **kwargs)

    def download_song(self, *args, **kwargs):
        return self.type_strategy.download_song(*args, **kwargs)

    def download_playlist(self, playlist: list, out: str = "output", compress: bool = False) -> None:
        out_path = Path(out)
        out_path.mkdir(exist_ok=True)

        for i, name in enumerate(playlist):
            if name:
                link_type = self.change_strategy_link(name)

                if link_type == TypePlaylist.SPOTIFY.value:
                    self.type_strategy.download_playlist(name, out)
                else:
                    with ThreadPoolExecutor(max_workers=10) as executor:
                        exe_results = [executor.submit(self.download_song, name, out)]

                        for exe in as_completed(exe_results):
                            try:
                                _ = exe.result()
                            except Exception as e:
                                print(f"Error: {e}")
                            print(f"({i + 1}/{len(playlist)}) {name}")

        if compress:
            with zipfile.ZipFile(f'{out}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipdir(out, zipf)
            shutil.rmtree(out)

    @property
    def type_strategy(self):
        return self._type_strategy

    @type_strategy.setter
    def type_strategy(self, index: int):
        self._type_strategy = self.__strategies[index]

    def change_strategy_link(self, link: str) -> int:
        link_type = recognition_link(link)
        self._type_strategy = self.__strategies.get(link_type, SongNamePlaylistFile())
        return link_type
