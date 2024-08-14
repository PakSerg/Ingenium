#!/bin/sh

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.5
done
sleep 10
echo "PostgreSQL is up!"

echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 0.5
done
echo "Redis is up!"

PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"

python generate_fixtures.py

python manage.py migrate
python manage.py loaddata questions/fixtures/category.json questions/fixtures/tag.json users/fixtures/user.json
python manage.py collectstatic --noinput

celery -A ingenium worker -l info -P eventlet &
# celery -A ingenium beat -l info &
celery -A ingenium flower -l info &
gunicorn ingenium.wsgi:application --bind 0.0.0.0:8000 &

wait