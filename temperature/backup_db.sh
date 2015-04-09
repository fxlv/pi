#!/bin/bash
#
# add something like: 
#    * * * * * cd ${HOME}/pi/temperature; ./backup_db.sh
# to your crontab
#
if ! sqlite3 temperature.db ".backup temperature.backup.db"; then
    sleep 5;
    sqlite3 temperature.db ".backup temperature.backup.db";
fi

cp temperature.backup.db /home/temperature/temperature.db
