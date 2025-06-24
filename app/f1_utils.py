import requests
import fastf1
from bs4 import BeautifulSoup
from datetime import datetime

def get_info_menu():
    return (
        "📋 Opciones:\n"
        "1. Clasificación pilotos\n"
        "2. Clasificación constructores\n"
        "3. Resultados última carrera\n"
        "4. Próxima carrera\n"
        "(Responde con 1, 2, 3 o 4)"
    )

def get_drivers_standings():
    url = "https://www.formula1.com/en/results.html/2025/drivers.html"
    response = requests.get(url)
    if response.status_code != 200:
        return "No se pudo obtener la clasificación de pilotos."

    soup = BeautifulSoup(response.text, "html.parser")
    table_rows = soup.select("table.f1-table tbody tr")

    msg = "🏁 Driver Standings (Top 5):\n"
    for i, row in enumerate(table_rows[:5]):
        cols = row.find_all("td")
        full_name = cols[1].text.strip()
        name = full_name[:-3].strip() if len(full_name) > 3 else full_name
        points = cols[-1].text.strip()
        msg += f"{i+1}. {name} – {points} pts\n"

    return msg

def get_constructors_standings():
    url = "https://www.formula1.com/en/results.html/2025/team.html"
    response = requests.get(url)
    if response.status_code != 200:
        return "No se pudo obtener la clasificación de constructores."

    soup = BeautifulSoup(response.text, "html.parser")
    table_rows = soup.select("table.f1-table tbody tr")

    msg = "🏆 Constructor Standings (Top 5):\n"
    for i, row in enumerate(table_rows[:5]):
        cols = row.find_all("td")
        team_name = cols[1].text.strip()
        points = cols[2].text.strip()
        msg += f"{i+1}. {team_name} – {points} pts\n"

    return msg

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
        return "No se pudo obtener el último podio de pilotos."
    
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
        return "No se pudo obtener la próxima carrera."