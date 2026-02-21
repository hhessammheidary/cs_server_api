#!/usr/bin/env bash
set -e
: "${UVICORN_HOST:=0.0.0.0}"
: "${UVICORN_PORT:=8000}"
echo "Starting uvicorn on ${UVICORN_HOST}:${UVICORN_PORT}"
exec uvicorn app.main:app --host "${UVICORN_HOST}" --port "${UVICORN_PORT}"
