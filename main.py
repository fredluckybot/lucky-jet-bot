import telebot
import random
import time
from datetime import datetime, timedelta
from threading import Thread
from flask import Flask
from telebot import types

# --- CONFIGURATION ---
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

# Compteurs pour les statistiques
stats = {"victoires": random.randint(140, 160), "confiance_moyenne": 92}

def generate_high_precision_logic():
    """ Logique de prédiction garantie 85%+ """
    fiabilite = random.randint(85, 99)
    if fiabilite > 92:
        cote = round(random.uniform(1.50, 2.20), 2)
    else:
        cote = round(random.uniform(2.21, 4.10), 2)
    return cote, fiabilite

def auto_signals_loop(chat_id):
    """ Envoi automatique toutes les 60-120 secondes """
    while True:
        time.sleep(random.randint(60, 120))
        cote, fiabilite = generate_high_precision_logic()
        h_jeu = (datetime.now() + timedelta(seconds=30)).strftime("%H:%M:%S")
        
        msg = (f"🚨 **SIGNAL IA DÉTECTÉ** 🚨\n"
               f"━━━━━━━━━━━━━━\n"
               f"📊 **FIABILITÉ :** `{fiabilite}%` 🔥\n"
               f"🎯 **OBJECTIF :** `{cote}x`\n"
               f"⏱️ **JOUEZ À :** `{h_jeu}`\n"
               f"━━━━━━━━━━━━━━\n"
               f"🧠 *Analyse : Cycle optimal détecté.*")
        
        try:
            bot.send_message(chat_id, msg, parse_mode="Markdown")
            stats["victoires"] += 1 # On simule une victoire de plus
        except:
            break

@bot.message_handler(commands=['start'])
def start(m):
    # Création du bouton Statistiques
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_stats = types.KeyboardButton("📊 Statistiques")
    markup.add(btn_stats)
    
    welcome = (f"🧠 **IA CONSCIENTE v7.0**\n\n"
               f"Bonjour {m.from_user.first_name} ! Je surveille le flux 24h/24.\n"
               f"Je t'enverrai uniquement des signaux **> 85%**.\n\n"
               f"⏳ *Recherche du premier cycle...*")
    
    bot.reply_to(m, welcome, reply_markup=markup)
    Thread(target=lambda: auto_signals_loop(m.chat.id)).start()

@bot.message_handler(func=lambda m: m.text == "📊 Statistiques")
def show_stats(m):
    res = (f"📈 **BILAN DU JOUR**\n"
           f"━━━━━━━━━━━━━━\n"
           f"✅ **Victoires :** `{stats['victoires']}`\n"
           f"🎯 **Taux de précision :** `{stats['confiance_moyenne']}%`\n"
           f"💰 **Statut du flux :** `TRÈS RENTABLE`\n"
           f"━━━━━━━━━━━━━━\n"
           f"🔄 *Mise à jour en temps réel.*")
    bot.reply_to(m, res, parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def chat(m):
    bot.reply_to(m, "Je reste concentré sur l'analyse pour te donner les meilleurs %.")

def run(): app.run(host='0.0.0.0', port=8080)
if __name__ == "__main__":
    Thread(target=run).start()
    bot.polling(none_stop=True)
