#!/bin/sh

set -euo pipefail

rm -f db.sqlite3
python3 manage.py migrate

gunicorn -c /etc/gunicorn/gunicorn.conf.py \
    hagiography.wsgi
