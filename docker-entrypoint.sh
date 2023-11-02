#!/bin/bash -x

if [ "$CELERY_FLOWER" = "no" ]
  then
  python manage.py migrate --noinput || exit 1
  python manage.py makesuperuser || exit 1
else
  python manage.py migrate --noinput || exit 1
fi

exec "$@"