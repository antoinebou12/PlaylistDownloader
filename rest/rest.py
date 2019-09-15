import os

from flask import Flask, request, send_from_directory
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from itertools import count
import configparser

from playlistdownloader.downloader import PlaylistDownloader, TypePlaylist

config = configparser.ConfigParser()
config.read('../config.ini')

COMPRESSION = bool(config['DEFAULT']['Compression'])
UPLOAD_FOLDER = config['DEFAULT']['UploadFolder']
DOWNLOAD_FOLDER = config['DEFAULT']['DownloadFolder']
ALLOWED_EXTENSIONS = set(['txt'])

# Spotipy Client ID
SPOTIPYCLIENTID = config['Spotify']['spotipyclientid']
SPOTIPYCLIENTSECRET = config['Spotify']['spotipyclientsecret']

tmpl_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'views')
static_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'public')

app = Flask(__name__, template_folder=tmpl_dir, static_folder=static_dir, static_url_path='')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

api = Api(app)

# TODO Change the rest api for not local file same on the server

class SoundCloudDownloader(Resource):

    _ids = count(0)

    def get(self, inputname):

        self._ids = next(self._ids)

        PLD_soundcloud = PlaylistDownloader("soundcloud", playlist_type=TypePlaylist.SOUNDCLOUD.value)
        soundcloud_list = PLD_soundcloud.load_playlist("{}/{}".format(UPLOAD_FOLDER, inputname))
        PLD_soundcloud.download_playlist(soundcloud_list, "download/soundcloud_%d/" % self._ids, compress=COMPRESSION)

        return {'fname': "soundcloud_%d.zip" % self._ids}


class YoutubeDownloader(Resource):

    _ids = count(0)

    def get(self, inputname):

        self._ids = next(self._ids)

        PLD_youtube = PlaylistDownloader(playlist_type=TypePlaylist.YOUTUBE.value)
        youtube_list = PLD_youtube.load_playlist("{}/{}".format(UPLOAD_FOLDER, inputname))
        PLD_youtube.download_playlist(youtube_list, "download/youtube_%d/" % self._ids, compress=COMPRESSION)

        return {'fname': "youtube_%d.zip" % self._ids}


class SpotifyDownloader(Resource):

    _ids = count(0)

    def get(self, inputname):

        self._ids = next(self._ids)

        PLD_spotify = PlaylistDownloader(playlist_type=TypePlaylist.SPOTIFY.value, spotipyid=SPOTIPYCLIENTID, spotipysecret=SPOTIPYCLIENTSECRET)
        spotify_list = PLD_spotify.load_playlist("{}/{}".format(UPLOAD_FOLDER, inputname))
        PLD_spotify.download_playlist(spotify_list, "download/spotify_%d/" % self._ids, compress=COMPRESSION)

        return {'fname': "spotify_%d.zip" % self._ids}


class Downloader(Resource):

    _ids = count(0)

    def get(self, inputname):

        self._ids = next(self._ids)

        PLD = PlaylistDownloader(spotipyid=SPOTIPYCLIENTID, spotipysecret=SPOTIPYCLIENTSECRET)
        playlist = PLD.load_playlist("{}/{}".format(UPLOAD_FOLDER, inputname))
        PLD.download_playlist(playlist, "download/downloader_%d" % self._ids, compress=COMPRESSION)

        return {'fname': "downloader_%d.zip" % self._ids}


class UploadFile(Resource):
    _ids = count(0)

    def post(self):
        file = None
        if 'file' in request.files:
            file = request.files['file']
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {
                'message': "Upload successful"
            }
        return {
            'message': "Invalid filename or extension (jpg, png, gif)"
        }

    @staticmethod
    def allowed_file(fname):
        return '.' in fname and fname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class ViewFile(Resource):
    _ids = count(0)

    def get(self, item):
        return send_from_directory(app.config['UPLOAD_FOLDER'], item)


class PlaylistDownloaded(Resource):
    _ids = count(0)

    def get(self, item):
        return send_from_directory(app.config['DOWNLOAD_FOLDER'], item)


api.add_resource(SoundCloudDownloader, '/api/soundcloud/<inputname>')
api.add_resource(YoutubeDownloader, '/api/youtube/<inputname>')
api.add_resource(SpotifyDownloader, '/api/spotify/<inputname>')
api.add_resource(Downloader, '/api/downloader/<inputname>')
api.add_resource(UploadFile, '/api/upload')
api.add_resource(ViewFile, '/api/view/<item>')
api.add_resource(PlaylistDownloaded, '/api/playlist/<item>')

if __name__ == '__main__':
    app.run(threaded=True)
