Minimal Stock Review Assistant (MVP)

Setup
1. Create virtual env and install:
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Copy .env.example -> .env and set NEWSAPI_KEY
   Get free key: https://newsapi.org/

3. Edit tickers.txt with tickers you want to scan.

Run
1. (optional) fetch data manually:
   python fetch_data.py tickers.txt

2. Start UI:
   streamlit run app.py

Notes
- Keep tickers list small on free tiers.
- The scoring is simple. Backtest before live trading.
