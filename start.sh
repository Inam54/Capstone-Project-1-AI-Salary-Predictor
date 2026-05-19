#!/bin/bash
streamlit run streamlit_app.py & 
uvicorn app:app --reload &
wait