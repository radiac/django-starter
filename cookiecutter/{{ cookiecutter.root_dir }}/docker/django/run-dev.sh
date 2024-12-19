#!/bin/bash
set -e

cd /project/

./manage.py migrate
./manage.py runserver 0:8000
