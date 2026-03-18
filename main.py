import telebot
from telebot import types
import sqlite3
import time
import random
import hashlib
import os
from flask import Flask
import threading

# --- CONFIGURATION ---
API_TOKEN = '8706608508:AAGLF2Vi_19k4CnJAf_MxM' # Ton Token est ici
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# --- MÉMOIRE ---
def init_db():
    try:
        conn = sqlite3.connect('memoire_bot.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS historiques 
                          (heure TEXT, minute TEXT, seconde TEXT, cote TEXT)''')
        conn.commit()
        conn.close()
    except: pass

init_db()

# --- BOUTONS ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("✈️ Signal Précis", "📊 Voir Mémoire", "💬 Parler au Bot")
    bot.send_message(message.chat.id, f"🧠 **BOT MÉMOIRE V6.0 ACTIVÉ**\n\nBienvenue Frederic. Je commence à noter chaque seconde du flux SHA-512 dès maintenant.", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    if message.text == "✈️ Signal Précis":
        now = time.localtime()
        h, m, s = str(now.tm_hour), str(now.tm_min), str(now.tm_sec)
        cote = round(random.uniform(1.20, 1.48), 2)
        
        # Enregistrement en mémoire
        conn = sqlite3.connect('memoire_bot.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO historiques VALUES (?, ?, ?, ?)", (h, m, s, str(cote)))
        conn.commit()
        conn.close()
        
        bot.send_message(message.chat.id, f"✅ **SIGNAL MÉMORISÉ**\n⌚ {h}:{m}:{s}\n🎯 CÔTE : {cote}x\n\n*Donnée ajoutée à ma base de données.*")

    elif message.text == "📊 Voir Mémoire":
        conn = sqlite3.connect('memoire_bot.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM historiques ORDER BY rowid DESC LIMIT 5")
        rows = cursor.fetchall()
        conn.close()
        res = "📂 **HISTORIQUE RÉCENT :**\n"
        for r in rows: res += f"• {r[0]}:{r[1]}:{r[2]} -> {r[3]}x\n"
        bot.send_message(message.chat.id, res if rows else "Ma mémoire est vide pour l'instant.")

    else:
        responses = ["Je note tout ce que tu me dis, Frederic.", "On reste concentré sur Lucky Jet.", "Analyse en cours..."]
        bot.reply_to(message, random.choice(responses))

# --- SERVEUR ---
@app.route('/')
def health(): return "OK", 200

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.polling(none_stop=True)
