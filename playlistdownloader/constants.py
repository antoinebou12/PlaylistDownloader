from enum import Enum

# File playlist enum
class TypePlaylist(Enum):
    # TODO change the playlist_type logic
    OTHER = -1
    SONG_NAME = 0
    SOUNDCLOUD = 1
    YOUTUBE = 2
    SPOTIFY = 3


TYPE_PLAYLIST = {
    'other': -1,
    'song_name': 0,
    'soundcloud': 1,
    'youtube': 2,
    'spotify': 3
}