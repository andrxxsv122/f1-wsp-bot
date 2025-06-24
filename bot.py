from flask import Flask, jsonify
from f1_utils import (
    get_drivers_standings,
    get_next_race,
    get_drivers_position,
    get_constructors_standings
)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Bot F1 API online 🚀", 200

@app.route("/api/info", methods=["GET"])
def info():
    reply = (
        "📋 Opciones:\n"
        "1. Clasificación pilotos\n"
        "2. Clasificación constructores\n"
        "3. Resultados última carrera\n"
        "4. Próxima carrera\n"
        "(Responde con 1, 2, 3 o 4)"
    )
    return jsonify({"message": reply})

@app.route("/api/option/<int:opt>", methods=["GET"])
def option(opt):
    if opt == 1:
        reply = get_drivers_standings()
    elif opt == 2:
        reply = get_constructors_standings()
    elif opt == 3:
        reply = get_drivers_position()
    elif opt == 4:
        reply = get_next_race()
    else:
        reply = "❌ Opción no válida. Escribe 'info' para ver el menú."
    return jsonify({"message": reply})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
