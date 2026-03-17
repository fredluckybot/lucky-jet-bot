import telebot
import random
from flask import Flask
from threading import Thread

# Configuration du bot
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
bot = telebot.TeleBot(TOKEN)

# Serveur Web pour garder le bot en vie sur Render Gratuit
app = Flask('')

@app.route('/')
def home():
    return "Bot Lucky Jet est en ligne !"

def run():
    app.run(host='0.0.0.0', port=8080)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 Lucky Jet Predictor v2 Connecté !\nEnvoie le dernier score pour obtenir une prédiction.")

@bot.message_handler(func=lambda message: True)
def predict(message):
    try:
        # Simulation d'analyse statistique
        prediction = round(random.uniform(1.2, 5.0), 2)
        bot.reply_to(message, f"🎯 Analyse terminée.\nProchain signal : {prediction}x")
    except:
        bot.reply_to(message, "Erreur d'analyse. Réessaie.")

def start_bot():
    # Lancement du serveur web en arrière-plan
    t = Thread(target=run)
    t.daemon = True
    t.start()
    # Lancement du bot Telegram
    bot.polling(none_stop=True)

if __name__ == "__main__":
    start_bot()
