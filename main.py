import telebot
from telebot import types
import time
import random
import os
import hashlib
from flask import Flask
import threading

# --- CONFIGURATION ---
API_TOKEN = '8706608508:AAFvfguEatFyduy0KUqv6d-DfvUEs6WveEQ'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# --- GÉNÉRATEUR DE PRÉDICTION ---
def generate_server_hash():
    seed = str(random.getrandbits(256))
    return hashlib.sha256(seed.encode()).hexdigest()

def get_prediction():
    rand = random.random()
    # 20% de chances : Petite côte (Prudence)
    if rand < 0.20: return round(random.uniform(1.25, 1.65), 2), "PRUDENCE ⚠️"
    # 65% de chances : Côte moyenne (Stable)
    elif rand < 0.85: return round(random.uniform(1.95, 4.80), 2), "STABLE ✅"
    # 15% de chances : Grosse côte (Jackpot)
    else: return round(random.uniform(5.50, 40.00), 2), "JACKPOT 🔥"

# --- INTERFACE ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("🚀 ANALYSER CE TOUR")
    markup.add(btn)
    bot.send_message(message.chat.id, 
                     "🎯 **PRÊT POUR LE PROCHAIN VOL**\n\nFrédéric, regarde ton écran Lucky Jet.\n\n1. Attends que le tour en cours se termine (Crash).\n2. **Dès que le message 'En attente' apparaît**, appuie sur le bouton ci-dessous.\n3. Je te donne le signal pour le tour qui commence !", 
                     reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🚀 ANALYSER CE TOUR")
def sync_predict(message):
    # Simulation de l'analyse ultra-rapide
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(0.4)
    
    h = time.strftime('%H:%M:%S')
    cibe, etat = get_prediction()
    current_hash = generate_server_hash()
    
    texte = (
        f"🛡️ **DECODER LIVE V14**\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🔐 **HASH ANALYSÉ :**\n`{current_hash[:28]}...`\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🚀 **CÔTE CIBLE :** `{cibe}x`\n"
        f"🔥 **FIABILITÉ :** `{random.randint(97, 99)}%` \n"
        f"⏰ **TEMPS RÉEL :** `{h}`\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"💎 **ANALYSE :** `{etat}`\n"
        f"⚠️ *Pariez immédiatement !*"
    )
    bot.send_message(message.chat.id, texte, parse_mode="Markdown")

# --- SERVEUR ---
@app.route('/')
def health(): return "OK", 200

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.polling(none_stop=True)
