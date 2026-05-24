#!/usr/bin/env bash
set -o errexit

python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input

if [ -n "$MEDIA_ROOT" ] && [ -d "mediafiles/products" ]; then
  mkdir -p "$MEDIA_ROOT/products"
  cp -R mediafiles/products/. "$MEDIA_ROOT/products/"
fi
