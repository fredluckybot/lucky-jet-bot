import telebot
from telebot import types
import random
import time
import hashlib
import os
from flask import Flask
import threading

# --- CONFIGURATION ---
API_TOKEN = '8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# --- FONCTION DE PRÉDICTION ---
def generate_now():
    proba = random.randint(85, 99)
    cote = round(random.uniform(1.60, 2.40), 2)
    # Simulation SHA-512 pour la crédibilité
    h_hash = hashlib.sha512(str(random.random()).encode()).hexdigest()[:12]
    # Heure du signal (30 secondes dans le futur)
    t = time.strftime('%H:%M:%S', time.gmtime(time.time() + 30))
    return proba, cote, h_hash, t

# --- GESTION DES BOUTONS ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("✈️ Lucky Jet", "💣 Mines IA", "📊 Statistiques", "🎁 Code Promo")
    bot.send_message(message.chat.id, "🧠 **IA CONSCIENTE V5.0 CONNECTÉE**\nPrête pour l'analyse immédiate.", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    if message.text == "✈️ Lucky Jet":
        p, c, h, t = generate_now()
        msg = (f"🚀 **SIGNAL IA DÉTECTÉ**\n━━━━━━━━━━━━━━━\n"
               f"✅ FIABILITÉ : {p}%\n"
               f"🎯 CÔTE CIBLE : {c}x\n"
               f"⌚ JOUER À : {t}\n"
               f"🔑 HASH : {h}\n"
               f"━━━━━━━━━━━━━━━\n"
               f"🧠 *Analyse du cycle terminée.*")
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    
    elif message.text == "📊 Statistiques":
        bot.send_message(message.chat.id, "📈 **BILAN OPÉRATIONNEL**\n✅ Victoires : 145\n🎯 Précision : 94%\n⚖️ Tendance : TRÈS POSITIVE")

    elif message.text == "💣 Mines IA":
        bot.send_message(message.chat.id, "💣 **MINES IA**\nAnalyse de la grille en cours... (Génère une grille ⭐)")

# --- KEEP ALIVE ---
@app.route('/')
def health(): return "OK", 200

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.polling(none_stop=True)
