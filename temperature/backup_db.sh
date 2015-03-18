#!/bin/bash
#
# add something like: 
#    * * * * * cd ${HOME}/pi/temperature; ./backup_db.sh
# to your crontab
#
sqlite3 temperature.db ".backup temperature.backup.db"
cp temperature.backup.db /home/temperature/temperature.db
