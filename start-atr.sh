#!/bin/bash
set -eu

# shellcheck source=/dev/null
source .venv/bin/activate

test -d /opt/atr/state || mkdir -p /opt/atr/state

if [ ! -f state/cert.pem ] || [ ! -f state/key.pem ]
then
  python3 scripts/generate-certificates
fi

mkdir -p /opt/atr/state/logs
echo "Starting hypercorn on ${BIND}" >> /opt/atr/state/logs/hypercorn.log
exec hypercorn --worker-class uvloop --bind "${BIND}" \
  --keyfile key.pem --certfile cert.pem atr.server:app >> /opt/atr/state/logs/hypercorn.log 2>&1
