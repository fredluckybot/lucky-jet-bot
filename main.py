import telebot
from telebot import types
import json
import os

# J'ai collé ton token proprement sans espaces
API_TOKEN = '8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg'
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
    bot.reply_to(message, "🚀 **IA LUCKY JET CONNECTÉE**\n\nFrédéric, envoie-moi le HASH du tour en cours pour commencer l'apprentissage !", parse_mode='Markdown')

@bot.message_handler(func=lambda message: len(message.text) > 30)
def analyser_hash(message):
    h = message.text.strip()
    user_last_hash[message.chat.id] = h
    memoire = charger_memoire()
    
    score = 0
    prefix = h[:5]
    for g in memoire["gagnes"]:
        if g.startswith(prefix): score += 1
    for p in memoire["perdus"]:
        if p.startswith(prefix): score -= 1
    
    if score > 0:
        res = "🟢 SIGNAL POSITIF"
    elif score < 0:
        res = "🔴 SIGNAL NÉGATIF"
    else:
        res = "🟡 ANALYSE NEUTRE (Nouveau Hash)"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ GAGNÉ", callback_data="gagne"),
               types.InlineKeyboardButton("❌ PERDU", callback_data="perdu"))
    
    bot.send_message(message.chat.id, f"**{res}**\n\nDis-moi le résultat du vol :", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    memoire = charger_memoire()
    h = user_last_hash.get(call.message.chat.id)
    if not h: return

    if call.data == "gagne":
        if h not in memoire["gagnes"]: memoire["gagnes"].append(h)
        bot.edit_message_text("✅ Enregistré comme GAGNANT.", call.message.chat.id, call.message.message_id)
    else:
        if h not in memoire["perdus"]: memoire["perdus"].append(h)
        bot.edit_message_text("❌ Enregistré comme PERDANT.", call.message.chat.id, call.message.message_id)
    sauvegarder_memoire(memoire)

bot.polling()
