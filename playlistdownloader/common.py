import os
import re

from playlistdownloader import TypePlaylist


def zipdir(path, ziph):
    """
    Create a zip directory and compress the file
    https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
    """

    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def invert_dict(dict):
    return {v: k for k, v in dict.items()}


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

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def progress_hook_ydl(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')