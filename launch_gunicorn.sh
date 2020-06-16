#!/bin/bash

NAME="danceapp"
PROJECTDIR=/www/backend
RUNDIR=$PROJECTDIR/run
SOCKFILE=$RUNDIR/gunicorn.sock
LOGFILE=$RUNDIR/gunicorn.log
ERRORFILE=$RUNDIR/gunicorn-error.log
LOGLEVEL=debug
USER=danceapp
GROUP=webapps
NUM_WORKERS=3
DJANGO_SETTINGSMODULE=$NAME.settings
DJANGO_WSGIMODULE=$NAME.wsgi

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
source `which virtualenvwrapper.sh`
cd $PROJECTDIR
workon $NAME
export DJANGO_SETTINGSMODULE=$DJANGO_SETTINGSMODULE
export PYTHONPATH=$PROJECTDIR:$PYTHONPATH

# Create the run directory if it doesn't exist
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
exec gunicorn ${DJANGO_WSGIMODULE}:application \
  --name=$NAME \
  --user=$USER \
  --group=$GROUP \
  --bind=unix:$SOCKFILE --workers=$NUM_WORKERS \
  --log-level=$LOGLEVEL --log-file=$LOGFILE 2>>$LOGFILE 1>>$ERRORFILE &

