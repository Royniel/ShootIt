from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ==============================
# Load API key
# ==============================
load_dotenv()
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env")

genai.configure(api_key=api_key)

# Flask app
app = Flask(__name__)

# Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Simple in-memory chat history
chat_history = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global chat_history
    user_input = request.json.get("message")
    print("User said:", user_input)  # Debug log

    try:
        # Add user input
        chat_history.append({"role": "user", "parts": [user_input]})

        # Get Gemini response
        response = model.generate_content(chat_history)
        bot_reply = response.text
        print("Bot replied:", bot_reply)  # Debug log

        # Add bot reply
        chat_history.append({"role": "model", "parts": [bot_reply]})

        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("⚠️ Error:", e)
        return jsonify({"reply": "⚠️ Error talking to Gemini."})


if __name__ == "__main__":
    app.run(debug=True)
