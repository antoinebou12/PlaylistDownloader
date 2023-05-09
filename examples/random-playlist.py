import typer
from rich.console import Console

from playlistdownloader.downloader import PlaylistDownloader
import configparser

config = configparser.ConfigParser()
config.read('spotipy_api_key.ini')

# Spotipy Client ID
SPOTIPYCLIENTID = config.get('SPOTIFY', 'spotipyclientid')
SPOTIPYCLIENTSECRET = config.get('SPOTIFY', 'spotipyclientsecret')

app = typer.Typer()

console = Console()

@app.command()
def main(
    input: str = typer.Argument(..., help='input file to check for new raw file'),
    output: str = typer.Option("youtube", help='output folder to check for new tiff file'),
    spotipyid: str = typer.Option(SPOTIPYCLIENTID, help='spotipy client-id'),
    spotipysecret: str = typer.Option(SPOTIPYCLIENTSECRET, help='spotipy client-secret'),
):
    PLD = PlaylistDownloader(spotipyid=spotipyid, spotipysecret=spotipysecret)
    # load the list of list
    song_list_link = PLD.load_playlist(input)

    PLD.download_playlist(song_list_link, out=output, compress=False)

    console.print("[green]Done![/green]")


if __name__ == "__main__":
    app()
