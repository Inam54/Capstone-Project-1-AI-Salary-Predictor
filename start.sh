#!/bin/bash
set -e

STREAMLIT_PORT="${PORT:-8501}"

uvicorn app:app --host 0.0.0.0 --port 8000 &

sleep 3

streamlit run streamlit_app.py --server.port "$STREAMLIT_PORT" --server.address 0.0.0.0 &

wait