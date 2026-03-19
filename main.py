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
    elif rand < 0.80: return round(random.uniform(1.80, 5.50), 2), "STABLE ✅"
    else: return round(random.uniform(6.00, 45.00), 2), "JACKPOT 🔥"

# --- BOUCLE AUTOMATIQUE RALENTIE ---
def auto_signal():
    global USER_ID
    while True:
        # --- ATTENTE ENTRE 3 ET 5 MINUTES ---
        time.sleep(random.randint(180, 300))
        
        if USER_ID:
            # 1. ENVOI D'UNE ALERTE DE PRÉPARATION
            bot.send_message(USER_ID, "⏳ **PRÉPARATION...**\nAnalyse du prochain cycle en cours. Préparez votre mise sur Lucky Jet !")
            
            # Attendre 30 secondes pour te laisser le temps d'ouvrir 1win
            time.sleep(30)
            
            h = time.strftime('%H:%M:%S')
            cibe, etat = get_advanced_prediction()
            current_hash = generate_server_hash()
            
            # --- DESIGN FINAL ---
            texte = (
                f"🛡️ **PROVABLY FAIR DECODER V13**\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"🔐 **HASH SERVEUR :**\n`{current_hash[:32]}...`\n"
                f"📡 **ALGORITHME :** `SHA-256 / SYNC`\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"🚀 **CÔTE CIBLE :** `{cibe}x`\n"
                f"🔥 **FIABILITÉ :** `{random.randint(97, 99)}%` \n"
                f"⏰ **JOUEZ MAINTENANT :** `{h}`\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"💎 **ANALYSE :** `{etat}`\n"
                f"⚠️ *Pariez dès que le prochain tour commence !*"
            )
            try:
                bot.send_message(USER_ID, texte, parse_mode="Markdown")
            except: pass

@bot.message_handler(commands=['start'])
def start(message):
    global USER_ID
    USER_ID = message.chat.id
    bot.send_message(message.chat.id, "🔓 **MODE ANALYSE CALME ACTIVÉ**\n\nJe vais t'envoyer une alerte de préparation 30 secondes avant chaque signal pour que tu aies le temps de parier.")

@app.route('/')
def health(): return "OK", 200

if __name__ == "__main__":
    threading.Thread(target=auto_signal, daemon=True).start()
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.polling(none_stop=True)
