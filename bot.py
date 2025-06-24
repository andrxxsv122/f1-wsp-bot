import sys
import os
sys.path.append(os.path.dirname(__file__))

from flask import Flask, request, jsonify
from f1_utils import get_drivers_standings, get_next_race

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "No se recibió JSON válido"}), 400

    message = data.get("message", {}).get("text", "").strip().lower()

    if message in ["start", "menu", "hola"]:
        reply = "📋 Opciones:\n1. Clasificación pilotos\n2. Próxima carrera\n(Responde con 1 o 2)"
    elif message == "1":
        reply = get_drivers_standings()
    elif message == "2":
        reply = get_next_race()
    else:
        reply = "❌ Opción no válida. Escribe 'hola' para ver el menú."

    return jsonify({
        "recipient_type": "individual",
        "type": "text",
        "text": {
            "body": reply
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)