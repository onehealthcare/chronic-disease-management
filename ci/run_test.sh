#!/bin/bash

# prepare
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWD -e "DROP DATABASE IF EXISTS $MYSQL_DB;"
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWD -e "CREATE DATABASE $MYSQL_DB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWD $MYSQL_DB < ci/tables.sql

py.test --cache-clear -vv -s --cov=models --cov=utils --cov-report=html tests/
