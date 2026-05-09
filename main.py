import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# RapidAPI Key (SportAPI)
RAPID_API_KEY = "5ca8651d88msh2bf5ae3df931be8p162c6ajsn11a0a0fc38d9"
HOST = "sportapi7.p.rapidapi.com"

@app.get("/matches/{date_str}")
def get_matches(date_str: str):
    url = f"https://{HOST}/api/v1/sport/football/scheduled-events/{date_str}"
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": HOST
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            events = response.json().get('events', [])
            data = []
            for e in events:
                data.append({
                    "id": e.get('id'),
                    "home": e.get('homeTeam', {}).get('name'),
                    "away": e.get('awayTeam', {}).get('name'),
                    "league": e.get('tournament', {}).get('name', 'League'),
                    "ai": {"prediction": "1", "exact_score": "2-1"}
                })
            return data
        return []
    except:
        return []

@app.get("/")
def root():
    return {"status": "ok"}
