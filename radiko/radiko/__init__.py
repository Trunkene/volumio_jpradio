# -*- config:utf-8 -*-

from flask import Flask, request, make_response, Response
from .radiko import Radiko
try:
    from settings import account
except:
    pass
from settings import defs
import os
import logging
from . import db
from .icymeta import IcyMetadata
from .prog import RdkProg

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.config.update(
        DATABASE=os.path.join(app.instance_path, defs.RADIKO_PGDBNAME)
    )
    logger = app.logger

    # For first gen_playlist
    playlist = {
        'url': defs.RADIKO_PLAYLIST_URL,
        'file': (defs.RADIKO_PLAYLIST_FILE_VOLUMIO if app.config['TGT_ENV'] == 'VOLUMIO' else defs.RADIKO_PLAYLIST_FILE_MPD)
    }
    try:
        act = {'mail': account.RADIKO_MAIL, 'pass': account.RADIKO_PASS}
    except:
        act = {}
    Radiko(app.config['TGT_ENV'], act, playlist, logger=logger)

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
        rdk = radiko.Radiko(app.config['TGT_ENV'], act, playlist, logger=logger)
        response = Response(rdk.play(station_id))
        response.content_type = "audio/aac"
        response.cache_control.no_cache = True
        response.cache_control.no_store = True
        response.headers['icy-name'] = rdk.getStationAsciiName(station_id)
        response.headers['icy-metaint'] = IcyMetadata.META_INT
        logger.debug('get returning response')
        return response

    def pgupdate():
        prg = RdkProg()
        prg.updatePrograms(Radiko.area)
        prg.clearOldProgram()

    @app.route('/radiko/pgupdate')
    def program_update():
        logger.debug(request)
        pgupdate()
        return 'OK'

    db.init_app(app)
    pgupdate()

    return app
