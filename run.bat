start cmd /k uvicorn app:app --reload
timeout /t 2
streamlit run dashboard.py
