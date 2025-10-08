# signals.py
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def compute_price_signals(price_df):
    df = price_df.copy().dropna().reset_index(drop=True)
    df["ret1"] = df["adj_close"].pct_change(1)
    df["ret5"] = df["adj_close"].pct_change(5)
    df["ret20"] = df["adj_close"].pct_change(20)
    vol = df["ret1"].std() * np.sqrt(252) if not df["ret1"].isna().all() else 0.0
    latest = df.iloc[-1]
    return {
        "last_price": float(latest["adj_close"]),
        "momentum_5": float(df["ret5"].iloc[-1]) if len(df)>5 else 0.0,
        "momentum_20": float(df["ret20"].iloc[-1]) if len(df)>20 else 0.0,
        "realized_vol_30": float(vol),
        "avg_volume": float(df["volume"].tail(30).mean()) if len(df)>0 else 0.0,
        "volume_latest": float(latest["volume"]),
    }

def headline_sentiment(headlines):
    if not headlines:
        return 0.0, 0
    scores = []
    for h in headlines:
        text = (h.get("title") or "") + ". " + (h.get("description") or "")
        s = analyzer.polarity_scores(text).get("compound",0.0)
        scores.append(s)
    return float(np.mean(scores)), len(scores)

def composite_score(signals):
    import pandas as pd
    df = pd.DataFrame.from_dict(signals, orient="index")
    for col in ["momentum_5","momentum_20","realized_vol_30","headline_sentiment","news_count"]:
        if col not in df.columns:
            df[col] = 0.0
    df["z_mom5"] = (df["momentum_5"] - df["momentum_5"].mean()) / (df["momentum_5"].std() or 1)
    df["z_sent"] = (df["headline_sentiment"] - df["headline_sentiment"].mean()) / (df["headline_sentiment"].std() or 1)
    df["z_vol"] = (df["realized_vol_30"] - df["realized_vol_30"].mean()) / (df["realized_vol_30"].std() or 1)
    df["score"] = 0.45 * df["z_mom5"] + 0.35 * df["z_sent"] - 0.20 * df["z_vol"]
    return df.sort_values("score", ascending=False)

if __name__ == "__main__":
    pass
