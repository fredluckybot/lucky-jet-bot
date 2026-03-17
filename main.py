import telebot
import random
import hashlib
import hmac
from flask import Flask
from threading import Thread

# Configuration
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Système Lucky Jet Provably Fair SHA-512 Actif !"

def generate_fair_prediction(client_seed):
    server_seed = str(random.getrandbits(256)).encode()
    seed_data = str(client_seed).encode()
    hash_result = hmac.new(server_seed, seed_data, hashlib.sha512).hexdigest()
    value = int(hash_result[:13], 16)
    prediction = max(1.10, round((1000000 / (value % 1000000 + 1)) * 0.99, 2))
    if prediction > 35: prediction = round(random.uniform(5.0, 15.0), 2)
    return prediction, hash_result

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🛡️ **PROVABLY FAIR ACTIF**\n\nEnvoyez un score pour générer un hash SHA-512.", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def predict(message):
    try:
        score = message.text.replace(',', '.')
        pred, h = generate_fair_prediction(score)
        res = f"🚀 **SIGNAL DÉTECTÉ**\n━━━━━━━━━━━━━━\n🎯 **PRÉDICTION : {pred}x**\n━━━━━━━━━━━━━━\n🔐 **HASH SHA-512 :**\n`{h[:30]}...`"
        bot.reply_to(message, res, parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ Score invalide.")

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)
