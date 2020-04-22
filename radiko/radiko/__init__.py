from flask import Flask, request, make_response, Response
from . import radiko
try:
    from settings import account
except:
    pass
from settings import defs
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    logger = app.logger

    # For first gen_playlist
    playlist = {
        'url': defs.RADIKO_PLAYLIST_URL,
        'file': defs.RADIKO_PLAYLIST_FILE
    }
    try:
        act = {'mail': account.RADIKO_MAIL, 'pass': account.RADIKO_PASS}
    except:
        act = {}
    radiko.Radiko(act, playlist, logger=logger)

    @app.route('/radiko')
    def index():
        return "Hello, world. You're at the radiko_app index."

    @app.route('/radiko/<station_id>')
    def station_view(station_id):
        logger.debug(request)
        #playlist = {
        #    'url': defs.RADIKO_PLAYLIST_URL,
        #    'file': defs.RADIKO_PLAYLIST_FILE
        #}
        #try:
        #    act = {'mail': account.RADIKO_MAIL, 'pass': account.RADIKO_PASS}
        #except:
        #    act = {}
        rdk = radiko.Radiko(act, playlist, logger=logger)
        response = Response(rdk.play(station_id))
        response.content_type = "audio/aac"
        response.cache_control.no_cache = True
        response.cache_control.no_store = True
        logger.debug('get returning response')
        return response

    return app
