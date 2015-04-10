#!/bin/bash
#
# add something like: 
#    * * * * * cd ${HOME}/pi/temperature; ./backup_db.sh
# to your crontab
#
function backup {
    sqlite3 temperature.db ".backup temperature.backup.db" 2>/dev/null;
}

# the database can be locked when new data is being imported
# so we use simple retry mechanism
while true; do
    if backup; then
        # if backup was successful, copy the backup file
        # to a place where it will be accessible by remote ssh
        cp temperature.backup.db /home/temperature/temperature.db
        exit 0
    else
        sleep 5
    fi
done
