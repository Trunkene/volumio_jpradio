#!/bin/bash
#
# Usage: dlradiko.sh <STATION_ID> <START_DATETIME> <END_DATETIME> <OUTFILENAME>
# START_DATETIME/ENDDATETIME: YYYYMMDDHHmm
#
APP_HOME=$HOME/radiko
VIRTUALENV_PATH=$APP_HOME/venv
source $VIRTUALENV_PATH/bin/activate
cd $APP_HOME
rm -f $3
python3 dlprog.py $*

