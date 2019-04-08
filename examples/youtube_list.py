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
        parser.add_argument("--output", default="youtube", type=str, help='output folder to check for new tiff file')

        return parser

    def args(self):
        # command line argument
        parser = self._parser()
        argcomplete.autocomplete(parser)
        self._args = self._parser().parse_args()

    def main(self):
        PLD_youtube = PlaylistDownloader(playlist_type=TypePlaylist.YOUTUBE.value)
        # load the list of list
        song_list_link = PLD_youtube.load_playlist(self._args.input)

        PLD_youtube.download_playlist(song_list_link, self._args.output, compress=True)

        PLD_youtube.type_strategy.clean_y_dl()


if __name__ == '__main__':
    Main()
