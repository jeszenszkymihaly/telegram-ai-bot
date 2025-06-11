import os
import json
from flask import Flask, request
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters


app = Flask(__name__)

# 🟡 TOKEN: Írd ide a saját bot tokenedet a BotFather-től
TOKEN = "7561209535:AAHMvq7j5SMscrfQajALHNjrnapZDeBzjLc"

bot = telegram.Bot(token=TOKEN)

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def start(update: Update, context):
    update.message.reply_text("Szia! Írj bármit, emlékezni fogok rá!")

def handle_message(update: Update, context):
    user_id = str(update.effective_user.id)
    user_msg = update.message.text

    memory = load_memory()
    history = memory.get(user_id, [])
    history.append(user_msg)
    memory[user_id] = history
    save_memory(memory)

    last_msg = history[-2] if len(history) > 1 else "Ez az első üzeneted!"
    response = f"Emlékszem, hogy ezt írtad korábban: {last_msg}\nMost ezt írtad: {user_msg}"
    update.message.reply_text(response)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    application.process_update(update)
    return "ok"

# Dispatcher beállítása
from telegram.ext import ApplicationBuilder
application = ApplicationBuilder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route("/")
def index():
    return "Noel AI bot működik!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
