#!/bin/bash
# Restore the database from a dump in the data dir
#
# Usage:
#   docker-compose exec postgres /project/docker/postgres/restore.sh <filename>
#

# If no filename specified, load from database.dump if found else database.sql
if [ -z "$1" ]; then
    if [ -f /data/database.dump ]; then
        FILENAME=database.dump
    else
        FILENAME=database.sql
    fi

else
    FILENAME="$1"
fi


if [[ $FILENAME =~ \.dump$ ]]; then
    # For a PostgreSQL custom-format dump:
    pg_restore --clean --if-exists --no-acl --verbose --format=custom --no-owner \
        --username=$POSTGRES_USER --dbname=$POSTGRES_DB /data/$FILENAME.dump
else
    # For an SQL dump created using dump.sh:
    psql --username=$POSTGRES_USER --dbname=$POSTGRES_DB --file=/data/$FILENAME
fi
