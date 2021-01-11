# -*- config:utf-8 -*-

from urllib import request
import xml.etree.ElementTree as ET
import sqlite3
from datetime import datetime, timedelta, timezone
from .db import get_db

JST = timezone(timedelta(hours=+9), 'JST')

class RdkProg():
    PROG_URL = 'http://radiko.jp/v3/program/station/date/{}/{}.xml'

    def __init__(self):
        self.db = None
        self.station = None
        self.lastdt = None
        self.progdata = None

    def __del__(self):
        if self.db:
            self.db.close()

    def getDb(self):
        if self.db is None:
            self.db = get_db()
        return self.db

    def getCurProgram(self, station):
        curdt = datetime.now(JST).strftime('%Y%m%d%H%M')
        if (station != self.station) or (curdt != self.lastdt):
            rv = None
            db = self.getDb()
            sql = 'select * from prog where station = ? and ft <= ? and tt >= ?'
            rv = db.execute(sql, (station, curdt, curdt)).fetchall()
            self.progdata = (rv[0] if rv else None)
        self.station = station
        self.lastdt = curdt
        return self.progdata

    def putProgram(self, dao):
        db = self.getDb()
        # Sqlite3 on volumio does not accept 'on conflict'
        #sql = 'insert into prog (station, id, ft, tt, title, pfm) values(?, ?, ?, ?, ?, ?) on conflict(id) do nothing'
        try:
            sql = 'insert into prog (station, id, ft, tt, title, pfm) values(?, ?, ?, ?, ?, ?)'
            db.execute(sql, (dao['station'], dao['id'], dao['ft'], dao['tt'], dao['title'], dao['pfm']))
            db.commit()
        except sqlite3.Error:
            db.rollback()

    def clearOldProgram(self):
        curdt = datetime.now(JST).strftime('%Y%m%d%H%M')
        db = self.getDb()
        try:
            sql = 'delete from prog where tt < ?'
            db.execute(sql,  (curdt, ))
            db.commit()
        except sqlite3.Error:
            db.rollback()

    def printAll(self):
        db = self.getDb()
        sql = 'select * from prog'
        c = db.execute(sql)
        print(c.fetchall())

    def updatePrograms(self, sid):
        curdt = datetime.now().strftime('%Y%m%d')
        url = RdkProg.PROG_URL.format(curdt, sid)

        xml = request.urlopen(url)

        xml_string = xml.read()
        root = ET.fromstring(xml_string)
        prog_data = []
        for stations in root:
            if stations.tag == 'stations':
                station = stations[0]
                station_id = station.attrib['id']
                for progs in station:
                    for prog in progs:
                        if prog.tag == 'prog':
                            prog_data = {}
                            prog_data['station'] = station_id
                            prog_data['id'] = station_id + prog.attrib['id']
                            prog_data['ft'] = prog.attrib['ft'][0:12]
                            prog_data['tt'] = prog.attrib['to'][0:12]
                            for e in prog:
                                if e.tag in ['title', 'pfm']:     
                                    value = e.text
                                    prog_data[e.tag] = value
                            self.putProgram(prog_data)
  
