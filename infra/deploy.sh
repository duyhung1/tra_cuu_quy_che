#!/usr/bin/env bash
# Deploy a tagged image set on the EC2 host (T-006).
#   ./deploy.sh sha-abc1234
# Run on the EC2 host from the directory containing docker-compose.prod.yml.
# Before every production deploy: run `make eval` against the current build.
set -euo pipefail

TAG="${1:?usage: deploy.sh <image-tag>}"
REGION="${AWS_REGION:-ap-southeast-1}"
SECRET_ID="${SECRET_ID:-tcqc/prod}"
DOMAIN="${DOMAIN:?set DOMAIN, e.g. tcqc.example.com}"
ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
export REGISTRY="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"
export TAG

echo "→ Writing .env from Secrets Manager (${SECRET_ID})"
umask 077
aws secretsmanager get-secret-value --region "$REGION" --secret-id "$SECRET_ID" \
  --query SecretString --output text \
  | python3 -c 'import json,sys; [print(f"{k}={v}") for k,v in json.load(sys.stdin).items()]' > .env

echo "→ Pulling images ${TAG}"
aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "$REGISTRY"
docker compose -f docker-compose.prod.yml pull

echo "→ Running migrations"
docker compose -f docker-compose.prod.yml run --rm api alembic upgrade head

echo "→ Starting services"
docker compose -f docker-compose.prod.yml up -d --remove-orphans

echo "→ Smoke test"
for i in $(seq 1 30); do
  if curl -fsS "https://${DOMAIN}/healthz" > /dev/null; then
    [ -f .current_tag ] && cp .current_tag .last_tag
    echo "$TAG" > .current_tag
    echo "✔ Deployed ${TAG}"
    exit 0
  fi
  sleep 5
done
echo "✘ Smoke test failed — run ./rollback.sh" >&2
exit 1
