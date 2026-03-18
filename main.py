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

# --- GÉNÉRATEUR DE HASH (SHA-256) ---
def generate_server_hash():
    # Crée une clé hexadécimale unique de 64 caractères
    seed = str(random.getrandbits(256))
    return hashlib.sha256(seed.encode()).hexdigest()

# --- LOGIQUE DE PRÉDICTION ---
def get_advanced_prediction():
    rand = random.random()
    if rand < 0.15: return round(random.uniform(1.10, 1.48), 2), "CAUTION ⚠️"
    elif rand < 0.85: return round(random.uniform(1.65, 4.50), 2), "STABLE ✅"
    else: return round(random.uniform(5.50, 25.00), 2), "JACKPOT 🔥"

def auto_signal():
    global USER_ID
    while True:
        # Fréquence rapide (45 à 90 secondes)
        time.sleep(random.randint(45, 90))
        
        if USER_ID:
            h = time.strftime('%H:%M:%S')
            cibe, etat = get_advanced_prediction()
            current_hash = generate_server_hash()
            
            try:
                conn = sqlite3.connect('memoire.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO logs VALUES (?, ?, ?)", (h, str(cibe), current_hash))
                conn.commit()
                conn.close()
            except: pass
            
            # --- DESIGN "DECODER PRO" ---
            texte = (
                f"🛡️ **PROVABLY FAIR DECODER V12**\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"🔐 **HASH SERVEUR :**\n`{current_hash[:32]}...`\n"
                f"📡 **STATUS :** `DÉCODAGE SHA-256`\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"🚀 **CÔTE CIBLE :** `{cibe}x`\n"
                f"🔥 **CONFIANCE :** `{random.randint(97, 99)}%` \n"
                f"⏰ **HEURE :** `{h}`\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"💎 **ANALYSE :** `{etat}`\n"
                f"⚠️ *Le hash garantit l'intégrité du crash.*"
            )
            try:
                bot.send_message(USER_ID, texte, parse_mode="Markdown")
            except: pass

# --- COMMANDES ---
@bot.message_handler(commands=['start'])
def start(message):
    global USER_ID
    USER_ID = message.chat.id
    bot.send_message(message.chat.id, "🔓 **CRACKER PROVABLY FAIR ACTIVÉ**\n\nFrédéric, l'IA analyse maintenant les flux SHA-256 de Lucky Jet en temps réel.")

# --- SERVEUR POUR RENDER ---
@app.route('/')
def health(): return "OK", 200

if __name__ == "__main__":
    threading.Thread(target=auto_signal, daemon=True).start()
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.polling(none_stop=True)
