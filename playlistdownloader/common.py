import os
import re
from zipfile import ZipFile

from playlistdownloader import TypePlaylist


def zipdir(path: str, ziph: ZipFile) -> None:
    """
    Create a zip directory and compress the file
    https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
    """

    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def recognition_link(link: str) -> str:
    main_url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', link)
    if not main_url:
        return TypePlaylist.SONG_NAME.value

    main_url = main_url[0]

    if main_url == 'https://soundcloud.com':
        return TypePlaylist.SOUNDCLOUD.value

    if main_url == 'https://www.youtube.com':
        if re.findall('(?<![\w\d])watch(?![\w\d])', link) or re.findall('(?<![\w\d])playlist(?![\w\d])', link):
            return TypePlaylist.YOUTUBE.value

    if main_url == 'https://open.spotify.com':
        return TypePlaylist.SPOTIFY.value

    return TypePlaylist.OTHER.value


class MyLogger:
    @staticmethod
    def debug(msg: str) -> None:
        pass

    @staticmethod
    def warning(msg: str) -> None:
        pass

    @staticmethod
    def error(msg: str) -> None:
        print(msg)


def progress_hook_ydl(d: dict) -> None:
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
