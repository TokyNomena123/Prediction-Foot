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

API_KEY = "7049f5254c9b3b10bcce95c62813293e"
URL = "https://v3.football.api-sports.io/fixtures"

@app.get("/matches/{date_str}")
def get_matches(date_str: str):
    headers = {'x-apisports-key': API_KEY}
    params = {'date': date_str}
    try:
        response = requests.get(URL, headers=headers, params=params, timeout=15)
        res = response.json()
        results = []
        for item in res.get('response', []):
            results.append({
                "id": item['fixture']['id'],
                "league": item['league']['name'],
                "league_logo": item['league']['logo'],
                "home": item['teams']['home']['name'],
                "home_logo": item['teams']['home']['logo'],
                "away": item['teams']['away']['name'],
                "away_logo": item['teams']['away']['logo'],
                "ai": {
                    "prediction": "1X",
                    "score": "2-1"
                }
            })
        return results
    except:
        return []

@app.get("/")
def root():
    return {"status": "ok"}
