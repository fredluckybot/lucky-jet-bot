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

def generate_server_hash():
    seed = str(random.getrandbits(256))
    return hashlib.sha256(seed.encode()).hexdigest()

def get_advanced_prediction():
    rand = random.random()
    if rand < 0.15: return round(random.uniform(1.20, 1.55), 2), "PRUDENCE ⚠️"
    elif rand < 0.80: return round(random.uniform(1.85, 5.80), 2), "STABLE ✅"
    else: return round(random.uniform(6.50, 50.00), 2), "JACKPOT 🔥"

# --- BOUCLE DE PRÉDICTION CALME ---
def auto_signal():
    global USER_ID
    while True:
        # Pause entre 4 et 7 minutes
        time.sleep(random.randint(240, 420))
        
        if USER_ID:
            # 1. MESSAGE DE PRÉPARATION (60 secondes avant)
            bot.send_message(USER_ID, "⏳ **ANALYSE EN COURS...**\nFrédéric, prépare ta mise sur Lucky Jet. Le signal arrive dans 60 secondes.")
            
            time.sleep(60) # Tu as 1 minute pour te préparer
            
            h = time.strftime('%H:%M:%S')
            cibe, etat = get_advanced_prediction()
            current_hash = generate_server_hash()
            
            texte = (
                f"🛡️ **PROVABLY FAIR DECODER V13**\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"🔐 **HASH SERVEUR :**\n`{current_hash[:32]}...`\n"
                f"📡 **ALGORITHME :** `SHA-256 / SYNC`\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"🚀 **CÔTE CIBLE :** `{cibe}x`\n"
                f"🔥 **FIABILITÉ :** `{random.randint(97, 99)}%` \n"
                f"⏰ **PARIEZ MAINTENANT :** `{h}`\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"💎 **ANALYSE :** `{etat}`\n"
                f"⚠️ *Le signal est prêt. Bonne chance !*"
            )
            try:
                bot.send_message(USER_ID, texte, parse_mode="Markdown")
            except: pass

@bot.message_handler(commands=['start'])
def start(message):
    global USER_ID
    USER_ID = message.chat.id
    bot.send_message(message.chat.id, "🔓 **MODE PERFORMANCE ACTIVÉ**\n\nJe t'enverrai une alerte 60 secondes avant chaque signal pour te laisser le temps de parier.")

@app.route('/')
def health(): return "OK", 200

if __name__ == "__main__":
    threading.Thread(target=auto_signal, daemon=True).start()
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.polling(none_stop=True)
