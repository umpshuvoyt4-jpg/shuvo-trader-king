import os, asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from signal_engine import get_signal, get_market_snapshot

SYMBOLS = os.getenv("SYMBOLS", "BTCUSDT,ETHUSDT").split(",")

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="Signal Board Starter", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home():
    return FileResponse("static/index.html")

@app.get("/api/signals")
async def signals():
    results = []
    for symbol in SYMBOLS:
        try:
            results.append(await asyncio.to_thread(get_signal, symbol.strip().upper()))
        except Exception as e:
            results.append({"symbol": symbol.strip().upper(), "direction": "WAIT",
                            "reason": f"Market data unavailable: {e}", "confidence": 0})
    return {"provider": "Binance public spot candles (demo feed)", "signals": results}

@app.get("/api/market/{symbol}")
async def market(symbol: str):
    return await asyncio.to_thread(get_market_snapshot, symbol.upper())
