import typer
import configparser

from playlistdownloader.downloader import PlaylistDownloader, TypePlaylist

config = configparser.ConfigParser()
config.read('../spotipy_api_key.ini')

# Spotipy Client ID
SPOTIPYCLIENTID = config['Spotify']['spotipyclientid']
SPOTIPYCLIENTSECRET = config['Spotify']['spotipyclientsecret']

app = typer.Typer()

@app.command()
def main(
    input: str = typer.Argument(..., help='link or filename'),
    output: str = typer.Option("spotify", help='output folder'),
    spotipyid: str = typer.Option(SPOTIPYCLIENTID, help='spotipy client-id'),
    spotipysecret: str = typer.Option(SPOTIPYCLIENTSECRET, help='spotipy client-secret'),
):
    PLD_spotify = PlaylistDownloader(
        playlist_type=TypePlaylist.SPOTIFY.value, spotipyid=spotipyid, spotipysecret=spotipysecret
    )

    playlist = PLD_spotify.load_playlist(input)

    PLD_spotify.download_playlist(playlist, out=output, compress=True)


if __name__ == "__main__":
    app()
