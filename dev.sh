#!/bin/bash

while [ 1 ]
do
#    gunicorn app:app --bind=$GUNICORN_BIND_ADDRESS --workers=$GUNICORN_WORKERS --log-level=$GUNICORN_LOG_LEVEL $GUNICORN_RELOAD --access-logfile=$GUNICORN_ACCESS_LOGFILE
    python3 app.py
    echo ''
    echo -e "\033[1;32m >>>>>> restart app, wait a moment... \033[0m"
    sleep 3

done
