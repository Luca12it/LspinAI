from flask import Flask, request, jsonify, send_file, send_from_directory
import subprocess
from prompts import SYSTEM_PROMPT

app = Flask(__name__, static_folder='.')

@app.route("/")
def home():
    return send_file("index.html")

# Nuova route per servire file statici (es. immagini)
@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory('images', filename)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Messaggio non valido."})

    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nUtente: {user_message}\nLspinAI:"
        
        result = subprocess.run(
            ["ollama", "run", "LspinAI"],  # <-- MODELLO MODIFICATO QUI
            input=full_prompt,
            capture_output=True,
            text=True,
            timeout=60,
            encoding='utf-8'
        )
        ai_response = result.stdout.strip()
    except Exception as e:
        ai_response = "Mi dispiace, c'è stato un errore nel processare la tua richiesta."

    return jsonify({"response": ai_response or "Nessuna risposta disponibile."})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)