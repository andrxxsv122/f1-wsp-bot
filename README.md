# 🏎️ F1 Info API

API REST para obtener información actualizada de Fórmula 1, pensada para integrarse con un bot de WhatsApp que responde consultas sobre:

- Clasificación de pilotos  
- Clasificación de constructores  
- Resultados de la última carrera  
- Próxima carrera

Esta API realiza scraping de la web oficial de Fórmula 1 y usa la librería FastF1 para datos específicos, exponiendo endpoints simples para consumir desde el bot.

---

## Tecnologías

- Python 3  
- Flask  
- FastF1  
- Requests  
- BeautifulSoup4

---

## Endpoints

- `GET /api/info`  
  Retorna el menú de opciones disponibles.

- `GET /api/option/<int:opt>`  
  Retorna la información según la opción seleccionada (1 a 4).

---

## Cómo usar

1. Clona el repo  
   ```bash
   git clone <url-del-repo>
   cd <nombre-del-repo>
   
2. Instala las dependencias  
   ```bash
   pip install -r requirements.txt
