import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "01d4ebfd5018479d9da7273412b399ba"

def get_ai_logic(home_name, away_name):
    # Poisson-based logic mock
    score_map = {
        "Real Madrid": 2.5, "Man City": 2.8, "Arsenal": 2.1, 
        "Barcelona": 1.9, "Liverpool": 2.3, "Bayern": 2.4
    }
    h_power = score_map.get(home_name, 1.5)
    a_power = score_map.get(away_name, 1.2)
    
    if h_power > a_power + 0.5:
        pred, exact = "1", f"{int(h_power)}-{int(a_power)}"
    elif a_power > h_power + 0.5:
        pred, exact = "2", f"{int(h_power)}-{int(a_power)}"
    else:
        pred, exact = "X", "1-1"
        
    return {"prediction": pred, "exact_score": exact, "confidence": "75%"}

@app.get("/matches/{date_str}")
def get_matches(date_str: str):
    url = f"https://api.football-data.org/v4/matches?dateFrom={date_str}&dateTo={date_str}"
    headers = {"X-Auth-Token": API_KEY}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            matches = response.json().get('matches', [])
            data = []
            for m in matches:
                home = m['homeTeam']['name']
                away = m['awayTeam']['name']
                data.append({
                    "id": m['id'],
                    "home": home,
                    "away": away,
                    "league": m['competition']['name'],
                    "status": m['status'],
                    "ai": get_ai_logic(home, away)
                })
            return data
        return []
    except:
        return []

@app.get("/")
def root():
    return {"status": "online"}
