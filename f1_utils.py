import os
from datetime import datetime
import fastf1
import requests

CACHE_DIR = 'cache'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

fastf1.Cache.enable_cache(CACHE_DIR)

SCRAPER_URL = "https://web-production-58e9a.up.railway.app"

def get_drivers_standings():
    try:
        res = requests.get(f"{SCRAPER_URL}/drivers")
        data = res.json()
        return data.get("message", "⚠️ No se pudo obtener la clasificación de pilotos.")
    except Exception as e:
        return f"⚠️ Error conectando al scraper: {e}"

def get_constructors_standings():
    try:
        res = requests.get(f"{SCRAPER_URL}/constructors")
        data = res.json()
        return data.get("message", "⚠️ No se pudo obtener la clasificación de constructores.")
    except Exception as e:
        return f"⚠️ Error conectando al scraper: {e}"
    
def get_drivers_position():
    try: 
        event = fastf1.get_event_schedule(2025)
        now = datetime.utcnow()
        last_round = event[event['EventDate'] < now].iloc[-1].RoundNumber
        session = fastf1.get_session(2025, last_round, 'R')
        session.load()
        results = session.results

        msg = "🏁 Top 3 Drivers (última carrera):\n"
        for i in range(min(3, len(results))):
            row = results.iloc[i]
            name = row.get('FullName') or row.get('Name') or row['Driver']
            points = row['Points']
            msg += f"{i+1}. {name} – {points} pts\n"
        return msg
    except Exception as e:
        print(f"Error en get_drivers_standings: {e}")
        return "No se pudo obtener la clasificación."
    
def get_next_race():
    try:
        schedule = fastf1.get_event_schedule(2025)
        now = datetime.utcnow()
        future_races = schedule[schedule['EventDate'] > now]
        if not future_races.empty:
            race = future_races.iloc[0]
            return f"🏎️ Próxima carrera:\n{race['EventName']} en {race['Country']} el {race['EventDate'].date()}"
        return "No se encontró la próxima carrera."
    except Exception as e:
        print(f"Error en get_next_race: {e}")
        return "No se pudo obtener la próxima carrera."
