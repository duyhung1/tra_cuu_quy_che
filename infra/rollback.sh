#!/usr/bin/env bash
# Redeploy the previous image tag (T-006).
set -euo pipefail
cd "$(dirname "$0")"
PREV="$(cat .last_tag 2>/dev/null || true)"
[ -n "$PREV" ] || { echo "No previous tag recorded (.last_tag missing)" >&2; exit 1; }
echo "Rolling back to ${PREV}"
exec ./deploy.sh "$PREV"
