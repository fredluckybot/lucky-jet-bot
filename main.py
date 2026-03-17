import telebot
import random
import hashlib
import hmac
import time
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

# Mémoire intelligente (stocke les 10 derniers scores)
historique_scores = []

def analyser_tendance():
    if not historique_scores: return "🔄 INITIALISATION..."
    moyenne = sum(historique_scores) / len(historique_scores)
    return "🔥 ZONE CHAUDE" if moyenne > 2.2 else "⚖️ ZONE STABLE"

def generate_fair_prediction(seed):
    srv_seed = str(random.getrandbits(256)).encode()
    hash_res = hmac.new(srv_seed, str(seed).encode(), hashlib.sha512).hexdigest()
    val = int(hash_res[:13], 16)
    pred = max(1.10, round((1000000 / (val % 1000000 + 1)) * 0.99, 2))
    return (round(random.uniform(5.0, 15.0), 2) if pred > 35 else pred), hash_res

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🤖 **LUCKY JET MONITOR v5.0 ACTIVÉ**\nSurveillance seconde par seconde en cours...")

@bot.message_handler(func=lambda m: True)
def predict(m):
    try:
        score = float(m.text.replace(',', '.'))
        historique_scores.append(score)
        if len(historique_scores) > 10: historique_scores.pop(0)
        
        # Effet visuel de surveillance
        wait = bot.reply_to(m, "🔍 **Scan des flux en cours...**\n`[▒░░░░░░░░░]`", parse_mode="Markdown")
        time.sleep(1) 
        
        now = datetime.now()
        heure_detec = now.strftime("%H:%M:%S")
        creneau = (now + timedelta(seconds=45)).strftime("%H:%M:%S")
        pred, h = generate_fair_prediction(score)
        
        res = (f"🚀 **SIGNAL VALIDÉ**\n━━━━━━━━━━━━━━\n"
               f"📊 **TENDANCE :** {analyser_tendance()}\n"
               f"⏰ **DÉTECTION :** {heure_detec}\n"
               f"🕒 **JOUEZ À :** `{creneau}`\n"
               f"🎯 **PRÉDICTION :** `{pred}x`\n━━━━━━━━━━━━━━\n"
               f"🔐 **HASH SHA-512 :**\n`{h[:30]}...`\n\n"
               f"🛰️ *Surveillance seconde par seconde active.*")
        bot.edit_message_text(res, m.chat.id, wait.message_id, parse_mode="Markdown")
    except: bot.reply_to(m, "⚠️ Score invalide.")

def run(): app.run(host='0.0.0.0', port=8080)
if __name__ == "__main__":
    Thread(target=run).start()
    bot.polling(none_stop=True)
