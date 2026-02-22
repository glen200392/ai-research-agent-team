#!/bin/sh
# docker-entrypoint.sh
# ─────────────────────────────────────────────────────────────────────────────
# Dual-mode entrypoint:
#   START_MODE=api  → start FastAPI server (for Fly.io / Docker API deployment)
#   START_MODE=cli  → run CLI pipeline (default, for scheduled runs)
#
# Usage inside container:
#   docker run --env-file .env -e START_MODE=api -p 8080:8080 image
#   docker run --env-file .env image team-a --month 2026-02
# ─────────────────────────────────────────────────────────────────────────────
set -e

case "${START_MODE:-cli}" in
  api)
    echo "[entrypoint] Starting FastAPI server on port ${PORT:-8080}"
    exec uvicorn api.server:app \
      --host 0.0.0.0 \
      --port "${PORT:-8080}" \
      --workers 2 \
      --log-level info
    ;;
  *)
    exec python run.py "$@"
    ;;
esac
