#!/usr/bin/env python3
import argparse
import argcomplete

from playlistdownloader.downloader import PlaylistDownloader, TypePlaylist

# Spotipy Client ID
SPOTIPYCLIENTID = "SPOTIPY_CLIENT_ID"
SPOTIPYCLIENTSECRET = "SPOTIPY_CLIENT_SECRET"


class Main(object):
    def __init__(self):
        super(Main, self).__init__()

        # main
        self.args()
        self.main()

        self._args = None

    @staticmethod
    def _parser():
        parser = argparse.ArgumentParser(description='.raw file to .tiff file format')
        parser.add_argument("input", type=str, help='link or filename')
        parser.add_argument("--output", default="spotify", type=str, help='output folder')
        parser.add_argument("--spotipyid", default=SPOTIPYCLIENTID, type=str,
                            help='spotipy client-id')
        parser.add_argument("--spotipysecret", default=SPOTIPYCLIENTSECRET, type=str,
                            help='spotipy client-secret')
        return parser

    def args(self):
        # command line argument
        parser = self._parser()
        argcomplete.autocomplete(parser)
        self._args = self._parser().parse_args()

    def main(self):
        PLD_spotify = PlaylistDownloader(playlist_type=TypePlaylist.SPOTIFY.value, spotipyid=self._args.spotipyid, spotipysecret=self._args.spotipysecret)

        playlist = PLD_spotify.load_playlist(self._args.input)

        PLD_spotify.download_playlist(playlist, out=self._args.output, compress=True)


if __name__ == '__main__':
    Main()
