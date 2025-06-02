from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import datetime

app = FastAPI()

class Signal(BaseModel):
    symbol: str
    profit: float
    side: str  # "buy" or "sell"

class Settings(BaseModel):
    trail: Optional[float] = 0.5
    rocket_mode: Optional[bool] = False
    save_ratio: Optional[float] = 0.5
    currency: Optional[str] = "USDT"

state = {
    "mode": "normal",
    "last_profit": 0.0,
    "rocket": False,
    "settings": {
        "trail": 0.5,
        "rocket_mode": False,
        "save_ratio": 0.5,
        "currency": "USDT"
    },
    "log": []
}

@app.post("/signal")
def receive_signal(signal: Signal):
    saved = signal.profit * state["settings"]["save_ratio"]
    reinvest = signal.profit - saved
    state["last_profit"] = signal.profit
    state["log"].append({
        "time": str(datetime.datetime.now()),
        "action": f"Received {signal.side} for {signal.symbol}",
        "profit": signal.profit,
        "saved": saved,
        "reinvest": reinvest
    })
    return {"status": "ok", "saved": saved, "reinvest": reinvest}

@app.post("/update-settings")
def update_settings(settings: Settings):
    state["settings"].update(settings.dict(exclude_unset=True))
    return {"status": "updated", "settings": state["settings"]}

@app.get("/status")
def get_status():
    return state

@app.get("/mode")
def get_mode():
    return {"mode": "🚀 rocket" if state["rocket"] else "⚙️ normal"}

@app.post("/toggle-rocket")
def toggle_rocket():
    state["rocket"] = not state["rocket"]
    return {"rocket": state["rocket"]}
