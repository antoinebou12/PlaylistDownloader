#!/usr/bin/env python3
import argparse
import argcomplete
import configparser

from playlistdownloader.downloader import PlaylistDownloader

config = configparser.ConfigParser()
config.read('../spotipy_api_key.ini')

# Spotipy Client ID
SPOTIPYCLIENTID = config['Spotify']['spotipyclientid']
SPOTIPYCLIENTSECRET = config['Spotify']['spotipyclientsecret']

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
        parser.add_argument("input", type=str, help='input file to check for new raw file')
        parser.add_argument("--output", default="youtube", type=str, help='output folder to check for new tiff file')
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
        PLD = PlaylistDownloader(spotipyid=self._args.spotipyid, spotipysecret=self._args.spotipysecret)
        # load the list of list
        song_list_link = PLD.load_playlist(self._args.input)

        PLD.download_playlist(song_list_link, out=self._args.output, compress=True)


if __name__ == '__main__':
    Main()
