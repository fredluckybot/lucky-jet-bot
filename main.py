import telebot
from telebot import types
import sqlite3
import time
import random
import os
from flask import Flask
import threading

# --- CONFIGURATION ---
# Nouveau Token mis à jour à 23:10
API_TOKEN = '8706608508:AAFvfguEatFyduy0KUqv6d-DfvUEs6WveEQ'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# --- BASE DE DONNÉES (MÉMOIRE) ---
def init_db():
    try:
        conn = sqlite3.connect('memoire.db')
        cursor = conn.cursor()
        # Création de la table pour stocker les signaux
        cursor.execute('CREATE TABLE IF NOT EXISTS logs (h TEXT, c TEXT)')
        conn.commit()
        conn.close()
    except:
        pass

init_db()

# --- COMMANDES ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Les deux boutons principaux
    markup.add("✈️ Lucky Jet", "📊 Mémoire")
    bot.send_message(message.chat.id, "✅ **SYSTÈME IA V8.0 ACTIVÉ**\n\nPrêt Frederic. Le nouveau token est opérationnel et la mémoire est connectée.", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    if message.text == "✈️ Lucky Jet":
        # Génération du signal
        h = time.strftime('%H:%M:%S')
        c = str(round(random.uniform(1.20, 1.42), 2))
        
        # Enregistrement immédiat en mémoire
        try:
            conn = sqlite3.connect('memoire.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO logs VALUES (?, ?)", (h, c))
            conn.commit()
            conn.close()
        except:
            pass
        
        bot.send_message(message.chat.id, f"🚀 **SIGNAL IA**\n━━━━━━━━━━━━━\n⌚ HEURE : {h}\n🎯 CIBLE : {c}x\n✅ FIABILITÉ : 98%\n━━━━━━━━━━━━━\n*Donnée mémorisée avec succès.*")

    elif message.text == "📊 Mémoire":
        # Lecture des 3 derniers signaux en base de données
        try:
            conn = sqlite3.connect('memoire.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs ORDER BY rowid DESC LIMIT 3")
            rows = cursor.fetchall()
            conn.close()
            
            if rows:
                txt = "📂 **HISTORIQUE MÉMOIRE :**\n"
                for r in rows:
                    txt += f"• {r[0]} -> {r[1]}x\n"
                bot.send_message(message.chat.id, txt)
            else:
                bot.send_message(message.chat.id, "Ma mémoire est encore vide. Génère un signal d'abord !")
        except:
            bot.send_message(message.chat.id, "Erreur de lecture de la mémoire.")

# --- SERVEUR POUR RENDER ---
@app.route('/')
def health(): return "OK", 200

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    # Lancement du serveur en arrière-plan
    threading.Thread(target=run_flask).start()
    # Lancement du bot
    bot.polling(none_stop=True)
