import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://www.sofascore.com/",
    "Origin": "https://www.sofascore.com"
}

def get_ai_prediction(event):
    return {
        "prediction": "1",
        "probability": {"1": 50, "X": 30, "2": 20},
        "exact_score": "2-1"
    }

@app.get("/matches/{date_str}")
def get_matches(date_str: str):
    url = f"https://api.sofascore.com/api/v1/sport/football/scheduled-events/{date_str}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            events = response.json().get('events', [])
            data = []
            for e in events:
                data.append({
                    "id": e.get('id'),
                    "home": e.get('homeTeam', {}).get('name'),
                    "away": e.get('awayTeam', {}).get('name'),
                    "h_score": e.get('homeScore', {}).get('current'),
                    "a_score": e.get('awayScore', {}).get('current'),
                    "status": e.get('status', {}).get('type'),
                    "league": e.get('tournament', {}).get('name'),
                    "ai": get_ai_prediction(e)
                })
            return data
        return {"error": "fetch_failed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"status": "online"}

