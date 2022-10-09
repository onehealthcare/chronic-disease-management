#!/bin/bash

export MYSQL_HOST=db
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWD=tonghs
export MYSQL_DB=cdm
export WXAPP_ID=your-wxapp-id
export WXAPP_SECRET=your-wxapp-secret
export JWT_SECRET=your-secret
export API_SECRET=your-secret
export GUNICORN_WORKERS=4
export GUNICORN_BIND_ADDRESS=0.0.0.0:5000
export GUNICORN_LOG_LEVEL=WARN
export GUNICORN_RELOAD=
export GUNICORN_ACCESS_LOGFILE=-
