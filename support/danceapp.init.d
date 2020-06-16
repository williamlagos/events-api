#!/bin/bash
# chkconfig: 345 99 10
# description: auto start danceapp application server
#
case "$1" in
 'start')
   su - danceapp -c "/www/backend/launch_gunicorn.sh"
   ;;
 'stop')
   killall gunicorn --verbose
   ;;
 'restart')
   killall gunicorn --verbose
   su - danceapp -c "/www/backend/launch_gunicorn.sh"
   ;;
 'status')
   echo "Listing gunicorn processes..."
   pgrep -l gunicorn
   ;;
esac
