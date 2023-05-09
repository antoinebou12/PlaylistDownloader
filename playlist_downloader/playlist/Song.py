import os

import youtube_dl

from playlist_downloader.playlist.PlaylistStrategy import PlaylistStrategyAbstract


class SongNamePlaylist(PlaylistStrategyAbstract):
    """
    Strategy used when there no link only a song name
    """

    def __init__(self):
        super().__init__()
        self.loaded_playlist = None

    def load_playlist(self, fname, decode="\n"):
        """

        :param fname:
        :param decode:
        :return:
        """
        if os.path.isfile(fname) and self.loaded_playlist is not None:
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
                [
                    "youtube-dl",
                    "--extract-audio",
                    "--audio-format",
                    "mp3",
                    "--audio-quality",
                    str(quality),
                    "-o",
                    f"{out}/%(title)s.%(ext)s",
                    link,
                    "--no-playlist",
                    "-i",
                    "--default-search",
                    "ytsearch",
                    "-q",
                    "--no-progress ",
                ]
            )
        except Exception:
            ydl_opts = {
                "outtmpl": f"{out}/%(title)s.%(ext)s",
                "verbose": False,
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
