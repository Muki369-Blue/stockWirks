# app.py
import os
import json
import streamlit as st
import pandas as pd
from fetch_data import fetch_all
from signals import compute_price_signals, headline_sentiment, composite_score
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Stock Review Assistant", layout="wide")

st.title("Wall Street Stock Review — MVP")

tickers_file = "tickers.txt"
if not os.path.exists(tickers_file):
    st.error("Create tickers.txt with one TICKER per line.")
    st.stop()
tickers = [l.strip().upper() for l in open(tickers_file) if l.strip()]

num_show = st.sidebar.slider("Top N", 1, min(20, len(tickers)), 7)
refresh = st.sidebar.button("Fetch latest data")

@st.cache_data(ttl=300)
def get_fetched(tickers):
    return fetch_all(tickers)

if refresh:
    st.sidebar.write("Fetching fresh data...")
data = get_fetched(tickers)

signals = {}
for t in tickers:
    entry = data.get(t, {})
    prices = entry.get("prices")
    headlines = entry.get("headlines", [])
    if isinstance(prices, str):
        try:
            prices = pd.read_csv(prices, parse_dates=["date"])
        except Exception:
            prices = None
    if prices is None:
        continue
    price_sig = compute_price_signals(prices)
    sent, nnews = headline_sentiment(headlines)
    price_sig.update({"headline_sentiment": sent, "news_count": nnews, "headlines": headlines})
    signals[t] = price_sig

if not signals:
    st.warning("No data fetched. Check NEWSAPI_KEY and network.")
    st.stop()

df_ranked = composite_score(signals)
st.subheader(f"Top {num_show} ranked tickers")
show_df = df_ranked[["last_price","momentum_5","momentum_20","realized_vol_30","headline_sentiment","news_count","score"]].head(num_show)
st.dataframe(show_df.style.format({
    "last_price":"${:,.2f}",
    "momentum_5":"{:.2%}",
    "momentum_20":"{:.2%}",
    "realized_vol_30":"{:.2%}",
    "headline_sentiment":"{:.3f}",
    "score":"{:.3f}"
}))

selected = st.sidebar.selectbox("Inspect ticker", list(df_ranked.index))
if selected:
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown(f"## {selected} — latest price ${signals[selected]['last_price']:.2f}")
        prices = data[selected]["prices"]
        prices = prices.set_index("date")
        st.line_chart(prices["adj_close"])
    with col2:
        st.markdown("### Top headlines")
        for h in signals[selected].get("headlines", []):
            st.markdown(f"- **{h.get('title')}**  \n  _{h.get('source')}_ — {h.get('publishedAt')}")
            st.markdown(f"  {h.get('url')}")
