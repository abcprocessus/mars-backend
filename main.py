from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

API_TOKEN = "MARS-4X7gVp9NzKLwT0C"

STATE = {
    "rocket_mode": False,
    "profit": 0,
    "copied": 0,
    "last_signal": "none",
    "config": {
        "copy_percent": 50,
        "limit_usdt": 100,
        "active": True
    }
}

def authorize(request: Request):
    token = request.query_params.get("token")
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/status")
def status(request: Request):
    authorize(request)
    return {
        "rocket_mode": STATE["rocket_mode"],
        "profit": STATE["profit"],
        "copied": STATE["copied"],
        "last_signal": STATE["last_signal"],
        "config": STATE["config"]
    }

@app.get("/signal")
def signal(request: Request, action: str = ""):
    authorize(request)
    STATE["last_signal"] = action
    return {"received_signal": action}

@app.get("/rocket")
def rocket(request: Request):
    authorize(request)
    STATE["rocket_mode"] = True
    return {"rocket_mode": "activated"}

@app.get("/save")
def save(request: Request):
    authorize(request)
    saved = int(STATE["profit"] * STATE["config"]["copy_percent"] / 100)
    STATE["copied"] += saved
    STATE["profit"] -= saved
    return {"saved": saved, "remaining": STATE["profit"]}

@app.get("/config")
def get_config(request: Request):
    authorize(request)
    return STATE["config"]
