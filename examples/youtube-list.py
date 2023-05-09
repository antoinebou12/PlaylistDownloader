import typer

from playlist_downloader.downloader import PlaylistDownloader
from playlist_downloader.downloader import TypePlaylist

app = typer.Typer()


@app.command()
def main(
    input: str = typer.Argument(..., help="input file to check for new raw file"),
    output: str = typer.Option(
        "youtube", help="output folder to check for new tiff file"
    ),
):
    PLD_youtube = PlaylistDownloader(playlist_type=TypePlaylist.YOUTUBE.value)
    # load the list of list
    song_list_link = PLD_youtube.load_playlist(input)

    PLD_youtube.download_playlist(song_list_link, output, compress=True)

    PLD_youtube.type_strategy.clean_y_dl()


if __name__ == "__main__":
    app()
