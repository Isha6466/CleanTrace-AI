#!/usr/bin/env bash
set -euo pipefail

gcloud run deploy cleantrace-ai --source . --region us-central1 --allow-unauthenticated --port 8080