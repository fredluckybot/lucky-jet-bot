import telebot
from telebot import types
import json
import os
from flask import Flask
from threading import Thread

# --- SERVEUR POUR RENDER ---
app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURATION ---
API_TOKEN = '8706608508:AAFvfguEatFyduy0KUqv6d-DfvUEs6WveEQ'
bot = telebot.TeleBot(API_TOKEN)
MEMOIRE_FILE = "memoire_hash.json"

def charger_memoire():
    if os.path.exists(MEMOIRE_FILE):
        try:
            with open(MEMOIRE_FILE, "r") as f: return json.load(f)
        except: return {"donnees": {}}
    return {"donnees": {}}

def sauvegarder_memoire(data):
    with open(MEMOIRE_FILE, "w") as f: json.dump(data, f)

user_last_hash = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 **IA LUCKY JET PRÉDICTEUR V2**\n\nEnvoyez-moi le HASH du tour pour obtenir une prédiction de côte !")

@bot.message_handler(func=lambda message: len(message.text) > 30)
def analyser_hash(message):
    h = message.text.strip()
    user_last_hash[message.chat.id] = h
    memoire = charger_memoire()
    prefix = h[:5] # Analyse les 5 premiers caractères
    
    stats = memoire["donnees"].get(prefix, {"gagnes": 0, "perdus": 0})
    total = stats["gagnes"] + stats["perdus"]
    
    # Calcul de la probabilité et de la côte cible
    if total > 0:
        win_rate = (stats["gagnes"] / total) * 100
        fiabilite = min(win_rate, 98) # Plafond à 98%
        cote_suggeree = round(1.2 + (win_rate / 40), 2)
    else:
        fiabilite = 50
        cote_suggeree = 1.50 # Côte par défaut pour un nouveau pattern

    res_text = (
        f"📊 **ANALYSE DU HASH**\n"
        f"🔑 Prefix: `{prefix}`\n\n"
        f"🎯 **CÔTE CIBLE : {cote_suggeree}x**\n"
        f"🔥 FIABILITÉ : {fiabilite:.1f}%\n\n"
        f"Le vol est-il monté au-dessus de {cote_suggeree}x ?"
    )
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ OUI (Gagné)", callback_data="gagne"),
               types.InlineKeyboardButton("❌ NON (Perdu)", callback_data="perdu"))
    
    bot.send_message(message.chat.id, res_text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    memoire = charger_memoire()
    h = user_last_hash.get(call.message.chat.id)
    if not h: return
    prefix = h[:5]

    if prefix not in memoire["donnees"]:
        memoire["donnees"][prefix] = {"gagnes": 0, "perdus": 0}

    if call.data == "gagne":
        memoire["donnees"][prefix]["gagnes"] += 1
    else:
        memoire["donnees"][prefix]["perdus"] += 1
    
    sauvegarder_memoire(memoire)
    bot.edit_message_text(f"✅ Merci ! Donnée enregistrée pour le pattern `{prefix}`. L'IA s'affine !", call.message.chat.id, call.message.message_id)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)
