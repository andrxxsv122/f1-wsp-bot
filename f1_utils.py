import os
from datetime import datetime
from zoneinfo import ZoneInfo
import fastf1

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CACHE_DIR = 'cache'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

fastf1.Cache.enable_cache(CACHE_DIR)

def get_drivers_standings():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        service = Service(r"C:\Sources\ChromeDriver\chromedriver.exe")  # Cambia la ruta aquí
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.formula1.com/en/results.html/2025/drivers.html")

        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.f1-table.f1-table-with-data.w-full tbody tr")))

        rows = driver.find_elements(By.CSS_SELECTOR, "table.f1-table.f1-table-with-data.w-full tbody tr")

        msg = "🏁 Driver Standings (Top 5):\n"
        for i in range(min(5, len(rows))):
            cols = rows[i].find_elements(By.TAG_NAME, "td")
            name = cols[1].text.strip() 
            points = cols[-1].text.strip()
            msg += f"{i+1}. {name} – {points} pts\n"

        driver.quit()
        return msg

    except Exception as e:
        return "No se pudo obtener la clasificación de pilotos."
    
def get_constructors_standings():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        service = Service(r"C:\Sources\ChromeDriver\chromedriver.exe")  # Cambia la ruta aquí
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.formula1.com/en/results.html/2025/team.html")

        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.f1-table.f1-table-with-data.w-full tbody tr")))

        rows = driver.find_elements(By.CSS_SELECTOR, "table.f1-table.f1-table-with-data.w-full tbody tr")

        msg = "🏆 Constructor Standings (Top 5):\n"
        for i in range(5):
            cols = rows[i].find_elements(By.TAG_NAME, "td")
            name = cols[1].text.strip()
            points = cols[2].text.strip()
            msg += f"{i+1}. {name} – {points} pts\n"

        driver.quit()
        return msg
    except Exception as e:
        return "No se pudo obtener la clasificación de constructores."

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
