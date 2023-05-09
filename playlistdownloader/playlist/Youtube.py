import os

import httpx
import youtube_dl
from bs4 import BeautifulSoup

from playlistdownloader.playlist.PlaylistStrategy import PlaylistStrategyAbstract


class YoutubePlaylistFile(PlaylistStrategyAbstract):
    """
    Strategy used for youtube link (normal video or playlist)
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
                    "-i",
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

    @staticmethod
    def write_youtube_playlist(url, out):
        """

        :param url:
        :param out:
        :return:
        """
        page = httpx.get(url)
        soup = BeautifulSoup(page.read(), "html.parser")
        href_tags = soup.find_all("a", {"class": "pl-video-title-link"}, href=True)

        with open(out, "w") as f:
            for i in href_tags:
                f.write("{}{}\n".format("https://www.youtube.com", i["href"]))
        f.close()

    @staticmethod
    def clean_y_dl():
        """
        TODO remove this method
        :return:
        """
        current = os.listdir(".")
        for file in current:
            if file.endswith(("mkv", "webm", ".part")):
                os.remove(file)
