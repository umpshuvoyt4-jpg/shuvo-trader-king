"""Educational EMA/RSI signal example. Not financial advice or a win guarantee."""
import json, urllib.request
from statistics import mean

BASE = "https://api.binance.com/api/v3/klines"

def candles(symbol="BTCUSDT", interval="1m", limit=100):
    url = f"{BASE}?symbol={symbol}&interval={interval}&limit={limit}"
    req = urllib.request.Request(url, headers={"User-Agent": "SignalBoardStarter/1.0"})
    with urllib.request.urlopen(req, timeout=12) as response:
        raw = json.loads(response.read().decode())
    return [{"close": float(x[4]), "open_time": int(x[0]), "close_time": int(x[6])} for x in raw]

def ema(values, period):
    alpha = 2 / (period + 1)
    result = values[0]
    for value in values[1:]:
        result = value * alpha + result * (1 - alpha)
    return result

def rsi(values, period=14):
    diffs = [values[i] - values[i-1] for i in range(1, len(values))]
    gains = [max(x, 0) for x in diffs[-period:]]
    losses = [max(-x, 0) for x in diffs[-period:]]
    avg_gain = mean(gains) if gains else 0
    avg_loss = mean(losses) if losses else 0
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def get_market_snapshot(symbol="BTCUSDT"):
    data = candles(symbol, "1m", 100)
    closes = [x["close"] for x in data[:-1]]  # exclude current unfinished candle
    return {"symbol": symbol, "price": closes[-1], "ema9": ema(closes[-40:], 9),
            "ema21": ema(closes[-60:], 21), "rsi14": rsi(closes)}

def get_signal(symbol="BTCUSDT"):
    snap = get_market_snapshot(symbol)
    fast, slow, strength = snap["ema9"], snap["ema21"], snap["rsi14"]
    direction, reason, confidence = "WAIT", "No clear setup; wait for confirmation.", 0
    if fast > slow and 50 < strength < 70:
        direction, reason, confidence = "UP", "EMA 9 is above EMA 21 and RSI has bullish momentum.", 60
    elif fast < slow and 30 < strength < 50:
        direction, reason, confidence = "DOWN", "EMA 9 is below EMA 21 and RSI has bearish momentum.", 60
    return {"symbol": symbol, "direction": direction, "price": snap["price"],
            "rsi": round(strength, 2), "ema9": round(fast, 6),
            "ema21": round(slow, 6), "confidence": confidence,
            "timeframe": "1m", "reason": reason,
            "source": "Binance public spot market"}
