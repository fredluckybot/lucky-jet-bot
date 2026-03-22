import telebot
from telebot import types
import json
import os
from flask import Flask
from threading import Thread

# --- SERVEUR POUR RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURATION DU BOT ---
# Ton nouveau Token valide
API_TOKEN = '8706608508:AAFvfguEatFyduy0KUqv6d-DfvUEs6WveEQ'
bot = telebot.TeleBot(API_TOKEN)
MEMOIRE_FILE = "memoire_hash.json"

def charger_memoire():
    if os.path.exists(MEMOIRE_FILE):
        try:
            with open(MEMOIRE_FILE, "r") as f:
                return json.load(f)
        except:
            return {"gagnes": [], "perdus": []}
    return {"gagnes": [], "perdus": []}

def sauvegarder_memoire(data):
    with open(MEMOIRE_FILE, "w") as f:
        json.dump(data, f)

user_last_hash = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 **IA LUCKY JET CONNECTÉE**\n\nFrédéric, envoie-moi le HASH du tour !")

@bot.message_handler(func=lambda message: len(message.text) > 30)
def analyser_hash(message):
    h = message.text.strip()
    user_last_hash[message.chat.id] = h
    memoire = charger_memoire()
    prefix = h[:5]
    
    score = sum(1 for g in memoire["gagnes"] if g.startswith(prefix)) - \
            sum(1 for p in memoire["perdus"] if p.startswith(prefix))
    
    res = "🟢 SIGNAL POSITIF" if score > 0 else "🔴 SIGNAL NÉGATIF" if score < 0 else "🟡 NOUVEAU HASH"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ GAGNÉ", callback_data="gagne"),
               types.InlineKeyboardButton("❌ PERDU", callback_data="perdu"))
    
    bot.send_message(message.chat.id, f"**{res}**\n\nRésultat du vol ?", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    memoire = charger_memoire()
    h = user_last_hash.get(call.message.chat.id)
    if not h: return

    if call.data == "gagne":
        if h not in memoire["gagnes"]: memoire["gagnes"].append(h)
    else:
        if h not in memoire["perdus"]: memoire["perdus"].append(h)
    
    sauvegarder_memoire(memoire)
    bot.edit_message_text(f"✅ Enregistré comme {call.data} !", call.message.chat.id, call.message.message_id)

# --- LANCEMENT ---
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("Bot démarré avec succès...")
    bot.polling(none_stop=True)
