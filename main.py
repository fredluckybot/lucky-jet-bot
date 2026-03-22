import telebot
from telebot import types
import json
import os

# TON TOKEN EST DÉJÀ INSÉRÉ ICI
API_TOKEN = '8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg'
bot = telebot.TeleBot(API_TOKEN)

# Fichier pour stocker la mémoire du bot (Apprentissage)
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

# Dictionnaire temporaire pour stocker le dernier hash envoyé par l'utilisateur
user_last_hash = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🚀 **LUCKY JET IA - MODE APPRENTISSAGE**\n\n"
        "Frédéric, envoie-moi le **HASH** du tour en cours.\n"
        "Je vais l'analyser et tu me diras si on gagne ou on perd pour m'éduquer !"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: len(message.text) > 30)
def analyser_hash(message):
    h = message.text.strip()
    user_last_hash[message.chat.id] = h
    memoire = charger_memoire()
    
    # Algorithme d'analyse par comparaison de début de Hash (les 5 premiers caractères)
    score = 0
    prefix = h[:5]
    
    for g in memoire["gagnes"]:
        if g.startswith(prefix): score += 1
    for p in memoire["perdus"]:
        if p.startswith(prefix): score -= 1
    
    # Prédiction basée sur l'historique enregistré
    if score > 0:
        prediction = "🟢 **ANALYSE : SIGNAL POSITIF** (Probabilité de hausse)"
    elif score < 0:
        prediction = "🔴 **ATTENTION : SIGNAL NÉGATIF** (Risque de crash bas)"
    else:
        prediction = "🟡 **ANALYSE : NEUTRE** (Pas encore de données sur ce type de Hash)"
    
    # Création des boutons de Feedback (Gagner/Perdre)
    markup = types.InlineKeyboardMarkup()
    btn_gagne = types.InlineKeyboardButton("✅ GAGNÉ", callback_data="gagne")
    btn_perdu = types.InlineKeyboardButton("❌ PERDU", callback_data="perdu")
    markup.add(btn_gagne, btn_perdu)
    
    bot.send_message(message.chat.id, f"{prediction}\n\nUne fois le tour fini, dis-moi le résultat :", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    memoire = charger_memoire()
    h = user_last_hash.get(call.message.chat.id)
    
    if not h:
        bot.answer_callback_query(call.id, "Erreur : Envoie un nouveau Hash d'abord.")
        return

    if call.data == "gagne":
        if h not in memoire["gagnes"]:
            memoire["gagnes"].append(h)
            sauvegarder_memoire(memoire)
        bot.edit_message_text("✅ **Noté !** J'ai enregistré ce Hash comme GAGNANT. Mon IA devient plus forte.", call.message.chat.id, call.message.message_id, parse_mode='Markdown')
    
    elif call.data == "perdu":
        if h not in memoire["perdus"]:
            memoire["perdus"].append(h)
            sauvegarder_memoire(memoire)
        bot.edit_message_text("❌ **C'est noté.** Hash enregistré comme PERDANT. Je t'avertirai si je revois un Hash similaire.", call.message.chat.id, call.message.message_id, parse_mode='Markdown')

bot.polling()
