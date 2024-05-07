#!/bin/sh

set -euo pipefail

if [ "$DEVELOPMENT" -eq "1" ]; then
    echo "Running server in development mode"
    cd /srv
    export DEFAULT_SERVER="reverse_proxy localhost:5173"

    yarn run dev &
fi

caddy run \
    --config /etc/caddy/Caddyfile \
    --adapter caddyfile
