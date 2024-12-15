#!/usr/bin/env bash

alembic upgrade head
uvicorn main:app --reload --host=0.0.0.0 --port 9090
exec "$@"