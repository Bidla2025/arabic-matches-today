from flask import Flask, render_template
import requests
from datetime import date
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY", "e86bae9172c1e6dc55f99be6068b5ae0")
LEAGUE_IDS = [39, 140, 135, 61, 78, 253, 235, 307]
COUNTRY_NAMES = {
    39: "الدوري الإنجليزي",
    140: "الدوري الإسباني",
    135: "الدوري الإيطالي",
    61: "الدوري الفرنسي",
    78: "الدوري الألماني",
    253: "الدوري المغربي",
    235: "الدوري المصري",
    307: "الدوري السعودي"
}

@app.route("/")
def index():
    today = date.today().strftime("%Y-%m-%d")
    headers = {"x-apisports-key": API_KEY}
    matches = []

    for league_id in LEAGUE_IDS:
        url = f"https://v3.football.api-sports.io/fixtures?date={today}&league={league_id}&season=2024"
        response = requests.get(url, headers=headers)
        data = response.json()

        for match in data.get("response", []):
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            logo_home = match['teams']['home']['logo']
            logo_away = match['teams']['away']['logo']
            start_time = match['fixture']['date']
            goals_home = match['goals']['home']
            goals_away = match['goals']['away']
            result = f"{goals_home}-{goals_away}" if goals_home is not None else "0-0"

            matches.append({
                "home": home,
                "away": away,
                "logo_home": logo_home,
                "logo_away": logo_away,
                "start_time": start_time,
                "result": result,
                "league": COUNTRY_NAMES[league_id]
            })

    return render_template("index.html", matches=matches)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
