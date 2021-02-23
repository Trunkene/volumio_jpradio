# -*- config:utf-8 -*-

import sys
import re
from logging import getLogger, StreamHandler, DEBUG
from radiko import Radiko

def show_usage():
    print('usage: {0} <station_id> <ft> <out_file>'.format(argv[0]))
    print('')
    print('station_id: Station ID (see http://radiko.jp/v3/station/region/full.xml)')
    print('ft: Record start datetime (%Y%m%d%H%M format, JST)')
    print('out_file: Output file path')

if __name__ == '__main__':
    argv = sys.argv

    if len(argv) != 4:
        show_usage()
        quit()
    
    if not re.match('[0-9]{12}', argv[2]):
        show_usage()
        quit()

    logger = getLogger(__name__)
    ch = StreamHandler()
    ch.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    logger.addHandler(ch)

    rdk = Radiko('VOLUMIO', {}, {}, False, logger)
    rdk.download(argv[1], argv[2] + '00', argv[3])
    del rdk