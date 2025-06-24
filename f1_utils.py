import os
import fastf1
import fastf1.utils

if not os.path.exists('cache'):
    os.mkdir('cache')

fastf1.Cache.enable_cache('cache')

def get_next_race():
    schedule = fastf1.get_event_schedule(2025)
    future_races = schedule[schedule['EventDate'] > fastf1.utils.current_datetime()]
    if not future_races.empty:
        race = future_races.iloc[0]
        return f"🏎️ Próxima carrera:\n{race['EventName']} en {race['Country']} el {race['EventDate'].date()}"
    return "No se encontró la próxima carrera."

def get_drivers_standings():
    try: 
        event = fastf1.get_event_schedule(2025)
        last_round = event[event['EventDate'] < fastf1.utils.current_datetime()].iloc[-1].RoundNumber
        session = fastf1.get_session(2025, last_round, 'R')
        session.load()
        results = session.results

        msg = "🏁 Top 3 Drivers (última carrera):\n"
        for i in range(3):
            row = results.iloc[i]
            name = f"{row.Driver.forename} {row.Driver.surname}"
            points = row.Points
            msg += f"{i+1}. {name} - {points} pts\n"
        return msg
    except:
        return "No se pudo obtener la clasificación."
