import os
import google.generativeai as genai
from dotenv import load_dotenv

# ==============================
# 1. Load API key from .env
# ==============================
load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("❌ No API key found. Please set GEMINI_API_KEY in your .env file.")

genai.configure(api_key=api_key)

# ==============================
# 2. Initialize Gemini model
# ==============================
model = genai.GenerativeModel("gemini-1.5-flash")

# Conversation memory
chat_history = []

print("🤖 Gemini Chatbot is ready! Type 'quit' to exit.\n")

# ==============================
# 3. Chat Loop
# ==============================
while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit"]:
        print("👋 Goodbye!")
        break

    # Add user input to history
    chat_history.append({"role": "user", "parts": [user_input]})

    try:
        # Generate response with context
        response = model.generate_content(chat_history)

        bot_reply = response.text
        print("Bot:", bot_reply)

        # Add bot reply to history
        chat_history.append({"role": "model", "parts": [bot_reply]})

    except Exception as e:
        print("⚠️ Error:", e)
