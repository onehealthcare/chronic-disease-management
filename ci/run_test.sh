#!/bin/bash

# prepare
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -e "DROP DATABASE IF EXISTS $MYSQL_DATABASE;"
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -e "CREATE DATABASE $MYSQL_DATABASE CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE < ci/tables.sql

py.test --cache-clear -vv -s --cov=models --cov=utils --cov-report=html tests/
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -e "DROP DATABASE IF EXISTS $MYSQL_DATABASE;"
exit $?
