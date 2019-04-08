#!/usr/bin/env python3
import argparse
import argcomplete

from playlistdownloader.downloader import PlaylistDownloader, TypePlaylist


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
        parser.add_argument("--output", default="soundcloud", type=str, help='output folder to check for new tiff file')

        return parser

    def args(self):
        # command line argument
        parser = self._parser()
        argcomplete.autocomplete(parser)
        self._args = self._parser().parse_args()

    def main(self):
        PLD_soundcloud = PlaylistDownloader("soundcloud", playlist_type=TypePlaylist.SOUNDCLOUD.value)
        song_list_link = PLD_soundcloud.load_playlist(self._args.input)
        PLD_soundcloud.download_playlist(song_list_link, self._args.output, compress=True)


if __name__ == '__main__':
    Main()