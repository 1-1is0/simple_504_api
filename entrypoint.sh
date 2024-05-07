#!/bin/bash
# chown -R www-data:www-data /app

# if [ "$DATABASE" = "postgres" ]
# then
i=0
echo "Waiting for Postgres... ${POSTGRES_HOST} ${POSTGRES_PORT}"
while ! nc -z ${POSTGRES_HOST} ${POSTGRES_PORT}; do
  echo "P${i}-"
  let "i+=1"
  sleep 1
done

# i=0
# echo "Waiting for Minio  ${RABBITMQ_HOST}:${RABBITMQ_MANAGMENT_PORT} ..."
# while ! nc -z ${RABBITMQ_HOST} ${RABBITMQ_MANAGMENT_PORT}; do
#   echo "R${i}-"
#   let "i+=1"
#   sleep 1
# done
# echo "RabbitMQ started"

sleep 1


echo "PostgreSQL started"
# fi

# python manage.py flush --no-input
echo "----- Collect static files ------ "
python manage.py collectstatic --noinput

echo "-----------Apply migration--------- "
# python manage.py makemigrations
python manage.py migrate

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    python manage.py createsuperuser --no-input --email $DJANGO_SUPERUSER_EMAIL --username $DJANGO_SUPERUSER_USERNAME
fi

# python manage.py runserver 0.0.0.0:8000
# gunicorn api.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3 & nginx -g "daemon off;"
# gunicorn -b :5000 --workers 5 api.wsgi:application

echo running "$@"
exec "$@"
