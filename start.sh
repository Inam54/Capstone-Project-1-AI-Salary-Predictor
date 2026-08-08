uvicorn app:app --host 0.0.0.0 --port 8000 &
streamlit run streamlit_app.py --server.port "$STREAMLIT_PORT" --server.address 0.0.0.0 &
wait