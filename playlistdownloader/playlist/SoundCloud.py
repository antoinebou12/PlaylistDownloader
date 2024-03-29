import os

import youtube_dl

from playlistdownloader.playlist.PlaylistStrategy import PlaylistStrategyAbstract


class SoundCloudPlaylist(PlaylistStrategyAbstract):
    """
    Strategy used for soundcloud link
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

    def download_song(self, link, out="."):
        """
        TODO change this to a scdl python function
        youtube-dl can do this also
        :param link:
        :param out:
        :return:
        """
        try:
            os.subprocess.call(
                [
                    "scdl",
                    "-l",
                    link,
                    "--path",
                    out,
                    "--onlymp3",
                    "-c",
                    "--error",
                    "--remove",
                ]
            )
        except Exception:
            try:
                os.subprocess.call(
                    [
                        "youtube-dl",
                        "--extract-audio",
                        "--audio-format",
                        "mp3",
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
