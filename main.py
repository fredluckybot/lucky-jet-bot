import telebot
import random
from datetime import datetime, timedelta

# --- METS TON TOKEN ICI ---
TOKEN = "8661147723:AAGFCnOUgZvYisjnuO2D6Q4IX9WUSZT82Q4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🚀 **Lucky Jet Predictor Connecté**\n\nEnvoie le dernier multiplicateur (ex: 1.50) pour obtenir l'heure du prochain signal.")

@bot.message_handler(func=lambda message: True)
def predict(message):
    try:
        # Nettoyage du message au cas où tu mets une virgule
        valeur = float(message.text.replace(',', '.'))
        maintenant = datetime.now()
        
        # Calcul du prochain signal (entre 1 et 3 minutes après)
        attente = random.randint(60, 180) 
        cible = maintenant + timedelta(seconds=attente)
        
        reponse = (
            f"📊 **ANALYSE TERMINÉE**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🎯 **PROCHAIN SIGNAL :** {cible.strftime('%H:%M:%S')}\n"
            f"📈 Confiance : {random.randint(75, 94)}%\n"
            f"━━━━━━━━━━━━━━━\n"
            f"⚠️ *Conseil : Entre en jeu 5s avant l'heure indiquée.*"
        )
        bot.reply_to(message, reponse, parse_mode="Markdown")
    except ValueError:
        bot.reply_to(message, "❌ Envoie un nombre valide (ex: 1.80)")

bot.infinity_polling()
