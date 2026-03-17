import telebot
import random

# Ton NOUVEAU Token Telegram
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 Lucky Jet Predictor v2 Connecté !\nEnvoie le dernier score (ex: 1.50).")

@bot.message_handler(func=lambda message: True)
def predict(message):
    try:
        valeur = float(message.text.replace(',', '.'))
        prediction = round(random.uniform(1.2, 5.0), 2)
        bot.reply_to(message, f"📊 Analyse pour {valeur}x\n🎯 Prochain signal : {prediction}x")
    except:
        bot.reply_to(message, "❌ Envoie un chiffre valide (ex: 2.10)")

bot.polling()
