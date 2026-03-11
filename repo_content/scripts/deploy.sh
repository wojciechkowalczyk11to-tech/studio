#!/usr/bin/env bash
set -euo pipefail

TAG="${1:-}"
if [[ -z "${TAG}" ]]; then
  TAG="$(git describe --tags --always)"
fi

: "${GCP_PROJECT_ID:?Ustaw zmienną GCP_PROJECT_ID w środowisku.}"
: "${GCP_REGION:?Ustaw zmienną GCP_REGION w środowisku.}"
: "${BACKEND_SERVICE_NAME:=nexus-backend}"

IMAGE="ghcr.io/${GITHUB_REPOSITORY_OWNER:-local}/nexus-omega-core-backend:${TAG}"

echo "[INFO] Budowanie obrazu backend: ${IMAGE}"
docker build -f Source/nexus-omega-core/infra/Dockerfile.backend -t "${IMAGE}" Source/nexus-omega-core

echo "[INFO] Wypychanie obrazu do GHCR"
docker push "${IMAGE}"

echo "[INFO] Wdrożenie do Cloud Run"
gcloud run deploy "${BACKEND_SERVICE_NAME}" \
  --project "${GCP_PROJECT_ID}" \
  --region "${GCP_REGION}" \
  --image "${IMAGE}" \
  --platform managed \
  --allow-unauthenticated

echo "[INFO] Wdrożenie zakończone pomyślnie"
