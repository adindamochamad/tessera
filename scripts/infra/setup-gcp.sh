#!/usr/bin/env bash
# Skrip bantu Day 1 — Google Cloud (jalankan dengan akun Anda yang sudah login gcloud).
set -euo pipefail

PROJECT_ID="${TESSERA_GCP_PROJECT:-tessera-hackathon}"
REGION="${TESSERA_GCP_REGION:-us-central1}"

echo "Tessera — setup GCP (proyek: ${PROJECT_ID})"
echo "Pastikan: gcloud auth login && billing aktif untuk hackathon credit."
echo ""

if ! command -v gcloud >/dev/null 2>&1; then
  echo "gcloud CLI tidak terpasang. Instal: https://cloud.google.com/sdk/docs/install"
  exit 1
fi

gcloud projects describe "${PROJECT_ID}" >/dev/null 2>&1 || \
  gcloud projects create "${PROJECT_ID}" --name="Tessera Hackathon"

gcloud config set project "${PROJECT_ID}"

APIS=(
  aiplatform.googleapis.com
  run.googleapis.com
  secretmanager.googleapis.com
  cloudbuild.googleapis.com
  iam.googleapis.com
)
for api in "${APIS[@]}"; do
  echo "Enable ${api}..."
  gcloud services enable "${api}" --project="${PROJECT_ID}"
done

SA_EMAIL="tessera-vertex@${PROJECT_ID}.iam.gserviceaccount.com"
if ! gcloud iam service-accounts describe "${SA_EMAIL}" --project="${PROJECT_ID}" >/dev/null 2>&1; then
  gcloud iam service-accounts create tessera-vertex \
    --display-name="Tessera Vertex AI" \
    --project="${PROJECT_ID}"
fi

for peran in roles/aiplatform.user roles/secretmanager.secretAccessor; do
  gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="${peran}" \
    --quiet >/dev/null
done

KEY_PATH="${TESSERA_SA_KEY:-./service-account.json}"
if [[ ! -f "${KEY_PATH}" ]]; then
  gcloud iam service-accounts keys create "${KEY_PATH}" \
    --iam-account="${SA_EMAIL}" \
    --project="${PROJECT_ID}"
  echo "Kunci disimpan: ${KEY_PATH} — jangan commit ke git."
fi

echo ""
echo "Selesai. Perbarui .env:"
echo "  GOOGLE_CLOUD_PROJECT=${PROJECT_ID}"
echo "  GOOGLE_APPLICATION_CREDENTIALS=${KEY_PATH}"
echo "  VERTEX_AI_LOCATION=${REGION}"
