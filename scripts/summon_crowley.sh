#!/bin/bash
PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/opt/aws/bin:/home/danceapp/.local/bin:/home/danceapp/bin

PROJECT_NAME="danceapp"
PROJECT_DIR=/www/backend
DJANGO_SETTINGSMODULE=$NAME.settings

echo "Summoning Crowley as `whoami`"

# Activate the virtual environment
source `which virtualenvwrapper.sh`
cd $PROJECT_DIR
workon $PROJECT_NAME
export DJANGO_SETTINGSMODULE=$DJANGO_SETTINGSMODULE
export PYTHONPATH=$PROJECTDIR:$PYTHONPATH

# Execute Crowley for owners
./manage.py crawl owner

deactivate
