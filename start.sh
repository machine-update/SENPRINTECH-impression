#!/usr/bin/env bash
set -o errexit

if [ -n "$MEDIA_ROOT" ] && [ -d "mediafiles/products" ]; then
  mkdir -p "$MEDIA_ROOT/products" || true
  cp -R mediafiles/products/. "$MEDIA_ROOT/products/" || true
fi

gunicorn ecommercesite.wsgi:application
