# fetch_data.py
import os
import time
import requests
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

NEWSAPI_URL = "https://newsapi.org/v2/everything"

def fetch_price_history(ticker, period="60d", interval="1d"):
    # explicit args to avoid warnings and racey cache behavior
    df = yf.download(
        ticker,
        period=period,
        interval=interval,
        progress=False,
        auto_adjust=True,
        threads=False,
    )
    if df is None or df.empty:
        return None

    # flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            ("_".join([str(p) for p in col if p is not None])).strip("_")
            for col in df.columns.values
        ]

    df = df.reset_index()

    # normalize column lookup (case-insensitive)
    colmap = {c.lower(): c for c in df.columns}

    # find adjusted/close column
    adj_candidates = ["adj close", "adj_close", "adjclose", "close"]
    adj_col = None
    for c in adj_candidates:
        if c in colmap:
            adj_col = colmap[c]
            break

    # find volume column
    vol_candidates = ["volume"]
    vol_col = None
    for c in vol_candidates:
        if c in colmap:
            vol_col = colmap[c]
            break

    # find date column
    date_candidates = ["date", "index"]
    date_col = None
    for c in date_candidates:
        if c in colmap:
            date_col = colmap[c]
            break
    if date_col is None:
        # fallback to first column if nothing matches
        date_col = df.columns[0]

    # rename to standard names; if missing volume set to 0
    rename_map = {}
    if adj_col:
        rename_map[adj_col] = "adj_close"
    elif "close" in df.columns:
        rename_map["close"] = "adj_close"

    rename_map[date_col] = "date"
    if vol_col:
        rename_map[vol_col] = "volume"

    df = df.rename(columns=rename_map)

    if "volume" not in df.columns:
        df["volume"] = 0

    # keep only the standardized columns
    if {"date", "adj_close", "volume"}.issubset(df.columns):
        return df[["date", "adj_close", "volume"]]
    else:
        return None

def fetch_headlines(ticker, page_size=5):
    if not NEWSAPI_KEY:
        return []
    params = {
        "q": ticker,
        "pageSize": page_size,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": NEWSAPI_KEY,
    }
    try:
        r = requests.get(NEWSAPI_URL, params=params, timeout=10)
        r.raise_for_status()
        items = r.json().get("articles", [])
        headlines = []
        for a in items:
            headlines.append({
                "title": a.get("title"),
                "description": a.get("description"),
                "source": a.get("source", {}).get("name"),
                "publishedAt": a.get("publishedAt"),
                "url": a.get("url")
            })
        return headlines
    except Exception:
        return []

def fetch_all(tickers):
    results = {}
    for t in tickers:
        prices = fetch_price_history(t)
        headlines = fetch_headlines(t, page_size=5)
        results[t] = {"prices": prices, "headlines": headlines}
        time.sleep(1)
    return results

if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 2:
        print("usage: python fetch_data.py tickers.txt")
        sys.exit(1)
    tickers = [l.strip().upper() for l in open(sys.argv[1]) if l.strip()]
    out = fetch_all(tickers)
    os.makedirs("data", exist_ok=True)
    for t,v in out.items():
        if v["prices"] is not None:
            v["prices"].to_csv(f"data/{t}_prices.csv", index=False)
        with open(f"data/{t}_headlines.json","w",encoding="utf-8") as f:
            json.dump(v["headlines"], f, ensure_ascii=False, indent=2)
    print("saved data/*")
