#!/bin/sh
set -eu

cd "$(dirname "$0")"

if [ -z "${1:-}" ]
then
  echo "Usage: $0 <test-pattern>"
  echo "Example: $0 sbom"
  exit 1
fi

echo "Running ATR e2e test: $1 (with reload)"

if ! docker compose ps atr-dev --status running -q 2>/dev/null | grep -q .
then
  echo "Starting ATR dev container..."
  docker compose up atr-dev -d --build --wait
fi

docker compose build e2e-dev
docker compose run --rm e2e-dev pytest "e2e/$1/" -v

echo "Use 'docker compose down atr-dev' to stop the dev container"
