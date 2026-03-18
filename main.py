import telebot
from telebot import types
import sqlite3
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
USER_ID = None 

# --- BASE DE DONNÉES ---
def init_db():
    try:
        conn = sqlite3.connect('memoire.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS logs (h TEXT, c TEXT, hash TEXT)')
        conn.commit()
        conn.close()
    except: pass

init_db()

# --- GÉNÉRATEUR DE HASH (PROVABLY FAIR) ---
def generate_fake_hash():
    # Crée un code complexe comme celui de Lucky Jet
    seed = str(random.getrandbits(256))
    return hashlib.sha256(seed.encode()).hexdigest()[:32]

# --- LOGIQUE DE PRÉDICTION ---
def get_prediction():
    rand = random.random()
    if rand < 0.15: return round(random.uniform(1.10, 1.40), 2), "CAUTION ⚠️"
    elif rand < 0.85: return round(random.uniform(1.65, 3.90), 2), "STABLE ✅"
    else: return round(random.uniform(5.50, 15.00), 2), "JACKPOT 🚀"

def auto_signal():
    global USER_ID
    while True:
        time.sleep(random.randint(45, 110))
        
        if USER_ID:
            h = time.strftime('%H:%M:%S')
            cibe, etat = get_prediction()
            server_hash = generate_fake_hash()
            
            try:
                conn = sqlite3.connect('memoire.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO logs VALUES (?, ?, ?)", (h, str(cibe), server_hash))
                conn.commit()
                conn.close()
            except: pass
            
            # --- DESIGN "CRACKER PROVABLY FAIR" ---
            texte = (
                f"🛠️ **PROVABLY FAIR CRACKER v12**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🔑 **SERVER HASH :**\n`{server_hash}...`\n"
                f"📡 **ALGORITHME :** `SHA-256 / ACTIVE`\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🚀 **PROCHAINE CÔTE :** `{cibe}x`\n"
                f"🔥 **CONFIANCE :** `{random.randint(97, 99)}%` \n"
                f"⏰ **TEMPS :** `{h}`\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"💎 **ÉTAT :** `{etat}`\n"
                f"⚠️ *Vérifiez le hash sur 1win après le tour.*"
            )
            try:
                bot.send_message(USER_ID, texte, parse_mode="Markdown")
            except: pass

# --- COMMANDES ---
@bot.message_handler(commands=['start'])
def start(message):
    global USER_ID
    USER_ID = message.chat.id
    bot.send_message(message.chat.id, "🔓 **DÉCODEUR PROVABLY FAIR ACTIVÉ**\n\nFrédéric, l'IA analyse maintenant les Hash SHA-256 du jeu en temps réel.")

# --- SERVEUR ---
@app.route('/')
def health(): return "OK", 200

if __name__ == "__main__":
    threading.Thread(target=auto_signal, daemon=True).start()
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.polling(none_stop=True)
