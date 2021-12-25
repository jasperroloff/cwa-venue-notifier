#!/bin/sh
set -e

until psql "$DATABASE_URL" -c '\l' > /dev/null 2>&1; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - continuing"

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
    python manage.py migrate --noinput
    python manage.py collectstatic --no-input --clear
    #python manage.py compilemessages
fi

exec "$@"
