import typer

from playlistdownloader.downloader import PlaylistDownloader
from playlistdownloader.downloader import TypePlaylist

app = typer.Typer()


@app.command()
def main(
    input: str = typer.Argument(..., help="input file to check for new raw file"),
    output: str = typer.Option(
        "soundcloud", help="output folder to check for new tiff file"
    ),
):
    PLD_soundcloud = PlaylistDownloader(
        "soundcloud", playlist_type=TypePlaylist.SOUNDCLOUD.value
    )
    song_list_link = PLD_soundcloud.load_playlist(input)
    PLD_soundcloud.download_playlist(song_list_link, output, compress=True)


if __name__ == "__main__":
    app()
