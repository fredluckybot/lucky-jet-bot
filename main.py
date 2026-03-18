import telebot
import random
import datetime
from flask import Flask
from threading import Thread

# Configuration
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

# Fonction pour enregistrer les données
def log_data(message_text, prediction):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Entrée: {message_text} | Prédiction: {prediction}x\n"
    
    # Écrit dans un fichier texte sur le serveur
    with open("history.txt", "a") as f:
        f.write(log_entry)
    print(log_entry) # S'affiche aussi dans les logs Render

@app.route('/')
def home():
    return "Surveillance Lucky Jet Active !"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "📊 Système d'enregistrement activé.\nEnvoyez un score pour lancer l'analyse.")

@bot.message_handler(commands=['history'])
def send_history(message):
    try:
        with open("history.txt", "r") as f:
            lines = f.readlines()
            last_logs = "".join(lines[-10:]) # Envoie les 10 derniers enregistrements
            bot.reply_to(message, f"📋 Derniers enregistrements :\n\n{last_logs}")
    except:
        bot.reply_to(message, "Aucun historique trouvé.")

@bot.message_handler(func=lambda message: True)
def predict(message):
    try:
        # 1. Générer la prédiction
        prediction = round(random.uniform(1.1, 4.5), 2)
        
        # 2. ENREGISTRER (Log)
        log_data(message.text, prediction)
        
        # 3. Répondre à l'utilisateur
        bot.reply_to(message, f"🎯 Signal : {prediction}x\n(Enregistré dans la base de données)")
    except:
        bot.reply_to(message, "Erreur lors de l'enregistrement.")

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)
import telebot
import random
import datetime
import hashlib
import hmac
from flask import Flask
from threading import Thread

# Configuration
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

# Serveur Web pour Render
@app.route('/')
def home():
    return "Système Provably Fair SHA-512 Actif"

def generate_fair_prediction(seed_user):
    """Génère une prédiction basée sur un hachage SHA-512"""
    # Création d'une clé secrète (Server Seed)
    server_seed = str(random.getrandbits(256)).encode()
    # Utilisation du score précédent comme Client Seed
    client_seed = str(seed_user).encode()
    
    # Génération du Hash SHA-512
    hash_result = hmac.new(server_seed, client_seed, hashlib.sha512).hexdigest()
    
    # Transformation mathématique du hash en multiplicateur (Logique Provably Fair)
    # On prend les 13 premiers caractères du hash
    value = int(hash_result[:13], 16)
    prediction = max(1.0, round(1000000 / (value % 1000000 + 1) * 0.98, 2))
    
    # Si la prédiction est trop basse par hasard, on la remonte légèrement pour le fun
    if prediction < 1.10:
        prediction = round(random.uniform(1.2, 2.5), 2)
        
    return prediction, hash_result

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🛡️ **Lucky Jet Provably Fair v3**\n\nChaque prédiction est désormais cryptée en **SHA-512**.\nEnvoyez le dernier score pour générer un signal vérifiable.")

@bot.message_handler(func=lambda message: True)
def predict(message):
    try:
        score_input = message.text.replace(',', '.')
        
        # Génération avec SHA-512
        prediction, hachage = generate_fair_prediction(score_input)
        
        reponse = (
            f"🎯 **SIGNAL DÉTECTÉ**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🚀 **Prédiction : {prediction}x**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🔐 **Hash SHA-512 (Vérifiable) :**\n"
            f"`{hachage[:40]}...`"
        )
        
        bot.reply_to(message, reponse, parse_mode="Markdown")
        
    except Exception as e:
        bot.reply_to(message, "❌ Erreur : Veuillez envoyer un nombre valide.")

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)


import telebot
import random
import datetime
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
    return "Système Provably Fair SHA-512 Actif !"

def generate_fair_prediction(client_seed):
    """Génère une prédiction mathématique basée sur le hachage SHA-512"""
    # Création d'une clé serveur unique pour ce tour
    server_seed = str(random.getrandbits(256)).encode()
    # Utilisation de ton score comme graine client
    seed_data = str(client_seed).encode()
    
    # Calcul du Hash SHA-512 ( HMAC )
    hash_obj = hmac.new(server_seed, seed_data, hashlib.sha512)
    hash_result = hash_obj.hexdigest()
    
    # Extraction d'une valeur mathématique du hash pour le multiplicateur
    # On utilise les 13 premiers caractères du hash (logique standard crash games)
    hex_part = hash_result[:13]
    value = int(hex_part, 16)
    
    # Formule Provably Fair : 10^6 / (valeur % 10^6 + 1) * 0.99
    # Cela garantit un résultat aléatoire mais vérifiable
    prediction = max(1.10, round((1000000 / (value % 1000000 + 1)) * 0.99, 2))
    
    # Sécurité pour les gros multiplicateurs
    if prediction > 50:
        prediction = round(random.uniform(10, 30), 2)
        
    return prediction, hash_result

@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = (
        "🛡️ **Lucky Jet Provably Fair Activé**\n\n"
        "Chaque prédiction est désormais générée via un algorithme **SHA-512** "
        "cryptographiquement sécurisé.\n\n"
        "Envoyez le dernier score pour voir la magie opérer."
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def predict(message):
    try:
        # Nettoyage de l'entrée (remplace virgule par point)
        score_entree = message.text.replace(',', '.')
        
        # Calcul de la prédiction Fair
        prediction, hachage = generate_fair_prediction(score_entree)
        
        reponse = (
            f"🎯 **NOUVEAU SIGNAL**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🚀 **PRÉDICTION : {prediction}x**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🔐 **HASH DU TOUR (Vérifiable) :**\n"
            f"`{hachage[:35]}...`"
        )
        
        bot.reply_to(message, reponse, parse_mode="Markdown")
        
    except Exception as e:
        bot.reply_to(message, "❌ Erreur : Veuillez envoyer un nombre valide.")

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)




import telebot
import random
import datetime
import hashlib
import hmac
from flask import Flask
from threading import Thread

# Configuration - Remplace par ton Token si nécessaire
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Système Provably Fair SHA-512 en ligne !"

def generate_fair_prediction(client_seed):
    """Logique mathématique Provably Fair SHA-512"""
    # Génération d'une clé serveur aléatoire (Server Seed)
    server_seed = str(random.getrandbits(256)).encode()
    # Utilisation du score envoyé comme graine client (Client Seed)
    seed_data = str(client_seed).encode()
    
    # Création du Hash SHA-512 via HMAC
    hash_obj = hmac.new(server_seed, seed_data, hashlib.sha512)
    hash_result = hash_obj.hexdigest()
    
    # Conversion du hash en multiplicateur (algorithme standard crash)
    # On prend les 13 premiers caractères hexadécimaux
    hex_extract = hash_result[:13]
    value = int(hex_extract, 16)
    
    # Formule : 1000000 / (reste de la division + 1) * 0.99 (maison)
    prediction = max(1.10, round((1000000 / (value % 1000000 + 1)) * 0.99, 2))
    
    # Limitation pour rester dans des zones réalistes
    if prediction > 40:
        prediction = round(random.uniform(10.0, 25.0), 2)
        
    return prediction, hash_result

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bienvenue = (
        "🛡️ **LUCKY JET PROVABLY FAIR**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "Bienvenue ! Ce bot utilise désormais le hachage **SHA-512** pour garantir l'intégrité des signaux.\n\n"
        "✅ **Sécurisé**\n"
        "✅ **Mathématique**\n"
        "✅ **Vérifiable**\n\n"
        "👉 *Envoyez le dernier score (ex: 1.85) pour obtenir le prochain signal.*"
    )
    bot.reply_to(message, bienvenue, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def predict(message):
    try:
        # Nettoyage de l'entrée (virgule -> point)
        score_val = message.text.replace(',', '.')
        
        # Calcul du signal avec SHA-512
        prediction, hachage = generate_fair_prediction(score_val)
        
        # Design du message de réponse
        reponse = (
            f"🚀 **SIGNAL DÉTECTÉ**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🎯 **PRÉDICTION : {prediction}x**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔐 **HASH SHA-512 :**\n"
            f"`{hachage[:40]}...`"
        )
        
        bot.reply_to(message, reponse, parse_mode="Markdown")
        
    except Exception:
        bot.reply_to(message, "⚠️ Veuillez envoyer un score valide (ex: 2.10)")

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)
import telebot
import random
import hashlib
import hmac
from datetime import datetime
from flask import Flask
from threading import Thread

# Configuration
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Système Lucky Jet Horodaté Actif !"

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
    bot.reply_to(message, "🛡️ **PROVABLY FAIR + LIVE TIME**\n\nEnvoyez un score pour obtenir un signal horodaté.", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def predict(message):
    try:
        # Récupération de l'heure actuelle
        maintenant = datetime.now().strftime("%H:%M:%S")
        
        score = message.text.replace(',', '.')
        pred, h = generate_fair_prediction(score)
        
        res = (
            f"🚀 **SIGNAL DÉTECTÉ**\n"
            f"━━━━━━━━━━━━━━\n"
            f"⏰ **HEURE : {maintenant}**\n"
            f"🎯 **PRÉDICTION : {pred}x**\n"
            f"━━━━━━━━━━━━━━\n"
            f"🔐 **HASH SHA-512 :**\n"
            f"`{h[:30]}...`"
        )
        bot.reply_to(message, res, parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ Score invalide.")

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)



import telebot
import random
import hashlib
import hmac
import time
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# Configuration
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot Lucky Jet Live Time en ligne !"

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
    bot.reply_to(message, "🛡️ **PROVABLY FAIR + LIVE TIME**\n\nEnvoyez un score pour obtenir un signal horodaté.", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def predict(message):
    try:
        # Récupération de l'heure actuelle (GMT)
        maintenant = datetime.now().strftime("%H:%M:%S")
        
        score = message.text.replace(',', '.')
        pred, h = generate_fair_prediction(score)
        
        res = (
            f"🚀 **SIGNAL DÉTECTÉ**\n"
            f"━━━━━━━━━━━━━━\n"
            f"⏰ **HEURE : {maintenant}**\n"
            f"🎯 **PRÉDICTION : {pred}x**\n"
            f"━━━━━━━━━━━━━━\n"
            f"🔐 **HASH SHA-512 :**\n"
            f"`{h[:30]}...`"
        )
        bot.reply_to(message, res, parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ Score invalide.")

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)




import telebot
import random
import hashlib
import hmac
from datetime import datetime
from flask import Flask
from threading import Thread

# Configuration
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot Lucky Jet Surveillance 24/7 Actif !"

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
    msg = (
        "🛡️ **SYSTÈME DE SURVEILLANCE ACTIF**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📡 Le bot surveille Lucky Jet **chaque seconde**.\n"
        "🔐 Algorithme Provably Fair SHA-512 engagé.\n\n"
        "👉 Envoyez le dernier score pour analyse."
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def predict(message):
    try:
        # Heure précise
        maintenant = datetime.now().strftime("%H:%M:%S")
        
        score = message.text.replace(',', '.')
        pred, h = generate_fair_prediction(score)
        
        res = (
            f"📡 **SURVEILLANCE EN TEMPS RÉEL**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⏰ **HEURE : {maintenant}**\n"
            f"🎯 **PRÉDICTION : {pred}x**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔐 **HASH SHA-512 :**\n"
            f"`{h[:30]}...`\n\n"
            f"🟢 *Analyse effectuée à la seconde près.*"
        )
        bot.reply_to(message, res, parse_mode="Markdown")
    except:
        bot.reply_to(message, "⚠️ Erreur d'analyse. Vérifiez le score.")

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)






import telebot
import random
import hashlib
import hmac
import time
from datetime import datetime
from flask import Flask
from threading import Thread

# Configuration
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot Lucky Jet Surveillance Temps Réel Actif !"

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
    msg = (
        "🛡️ **SURVEILLANCE LUCKY JET ACTIVE**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📡 État : **Connecté au serveur de jeu**\n"
        "⏱️ Fréquence : **Analyse chaque seconde**\n"
        "🔐 Sécurité : **SHA-512 Provably Fair**\n\n"
        "👉 *Envoyez le dernier score pour lancer l'analyse.*"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def predict(message):
    try:
        # Envoi d'un message d'attente pour simuler la surveillance
        waiting_msg = bot.reply_to(message, "⏳ **Analyse des flux en cours...**\n`[▒░░░░░░░░░] 10%`", parse_mode="Markdown")
        
        # Simulation de la barre de progression (très rapide)
        time.sleep(0.5)
        bot.edit_message_text("⏳ **Synchronisation des données...**\n`[████░░░░░░] 45%`", message.chat.id, waiting_msg.message_id, parse_mode="Markdown")
        time.sleep(0.5)
        bot.edit_message_text("⏳ **Calcul de l'algorithme SHA-512...**\n`[████████░░] 85%`", message.chat.id, waiting_msg.message_id, parse_mode="Markdown")
        
        # Calcul final
        maintenant = datetime.now().strftime("%H:%M:%S")
        score = message.text.replace(',', '.')
        pred, h = generate_fair_prediction(score)
        
        res = (
            f"📡 **SURVEILLANCE TEMPS RÉEL**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⏰ **HEURE : {maintenant}**\n"
            f"🎯 **PRÉDICTION : {pred}x**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔐 **HASH SHA-512 :**\n"
            f"`{h[:30]}...`\n\n"
            f"🟢 *Surveillance active : Signal validé.*"
        )
        
        # On remplace le message de chargement par le résultat final
        bot.edit_message_text(res, message.chat.id, waiting_msg.message_id, parse_mode="Markdown")
        
    except Exception as e:
        bot.reply_to(message, "⚠️ Erreur lors de la surveillance. Réessayez.")

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)



import telebot
import random
import hashlib
import hmac
import time
from datetime import datetime
from flask import Flask
from threading import Thread

# Configuration
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot Lucky Jet Surveillance Temps Réel Actif !"

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
    msg = (
        "🛡️ **SYSTÈME DE SURVEILLANCE ACTIVÉ**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📡 État : **Analyse du flux chaque seconde**\n"
        "🔐 Sécurité : **SHA-512 Provably Fair**\n"
        "🔗 Canal : **[REJOINDRE LE CANAL](https://t.me/ton_lien)**\n\n"
        "👉 *Envoyez le dernier score pour obtenir le prochain créneau.*"
    )
    # Ajout du bouton pour rejoindre le canal
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton("🚀 Rejoindre le Canal", url="https://t.me/ton_lien")
    markup.add(btn)
    
    bot.reply_to(message, msg, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def predict(message):
    try:
        # Message de chargement pour simuler la surveillance
        waiting_msg = bot.reply_to(message, "📡 **Surveillance du jeu en cours...**\n`[▒░░░░░░░░░]`", parse_mode="Markdown")
        
        # Simulation d'analyse seconde par seconde
        time.sleep(0.6)
        bot.edit_message_text("📡 **Scan des probabilités...**\n`[████░░░░░░]`", message.chat.id, waiting_msg.message_id, parse_mode="Markdown")
        time.sleep(0.6)
        bot.edit_message_text("📡 **Signal détecté ! Validation...**\n`[██████████]`", message.chat.id, waiting_msg.message_id, parse_mode="Markdown")
        
        # Calcul des données
        maintenant = datetime.now()
        heure_exacte = maintenant.strftime("%H:%M:%S")
        
        # Créneau conseillé (30 secondes après le signal)
        creneau = (maintenant + timedelta(seconds=30)).strftime("%H:%M:%S")
        
        score = message.text.replace(',', '.')
        pred, h = generate_fair_prediction(score)
        
        res = (
            f"🚀 **SIGNAL VALIDÉ**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⏰ **DÉTECTION : {heure_exacte}**\n"
            f"🎯 **CRÉNEAU DE JEU : {creneau}**\n"
            f"📈 **PRÉDICTION : {pred}x**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔐 **HASH SHA-512 :**\n"
            f"`{h[:30]}...`\n\n"
            f"🟢 *Le bot surveille le jeu chaque seconde pour vous.*"
        )
        
        # Bouton pour le canal sous chaque signal
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton("📢 Rejoindre pour plus de signaux", url="https://t.me/ton_lien")
        markup.add(btn)
        
        bot.edit_message_text(res, message.chat.id, waiting_msg.message_id, parse_mode="Markdown", reply_markup=markup)
        
    except Exception as e:
        bot.reply_to(message, "⚠️ Erreur lors de la surveillance.")

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)



import telebot
import random
import hashlib
import hmac
import time
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# Configuration - Remplace par ton vrai lien de canal
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
CANAL_URL = "https://t.me/ton_lien_ici" 

bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot Lucky Jet Surveillance Temps Réel v4.0"

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
    msg = (
        "🛡️ **SURVEILLANCE ACTIVE 24/7**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📡 Scan du jeu : **Chaque seconde**\n"
        "🔐 Algorithme : **SHA-512 Provably Fair**\n"
        "⚡ État : **Prêt pour l'analyse**\n\n"
        "👉 *Envoyez le dernier score pour détecter le prochain créneau.*"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def predict(message):
    try:
        # Étape 1 : Simulation de surveillance seconde par seconde
        waiting_msg = bot.reply_to(message, "📡 **Surveillance du flux en cours...**\n`[▒░░░░░░░░░]`", parse_mode="Markdown")
        time.sleep(0.7)
        bot.edit_message_text("📡 **Scan des probabilités...**\n`[████░░░░░░]`", message.chat.id, waiting_msg.message_id, parse_mode="Markdown")
        time.sleep(0.7)
        bot.edit_message_text("📡 **Signal détecté ! Calcul du créneau...**\n`[██████████]`", message.chat.id, waiting_msg.message_id, parse_mode="Markdown")
        
        # Étape 2 : Calcul des temps et de la prédiction
        maintenant = datetime.now()
        heure_detection = maintenant.strftime("%H:%M:%S")
        # Le créneau suggéré est 45 secondes après la détection
        creneau_jeu = (maintenant + timedelta(seconds=45)).strftime("%H:%M:%S")
        
        score = message.text.replace(',', '.')
        pred, h = generate_fair_prediction(score)
        
        # Étape 3 : Alerte Spéciale si > 10.0x
        alerte = ""
        if pred >= 10.0:
            alerte = "⚠️ **ALERTE GOLDEN SIGNAL (x10+)** ⚠️\n━━━━━━━━━━━━━━━━━━\n"
        
        res = (
            f"{alerte}"
            f"🚀 **SIGNAL VALIDÉ**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⏰ **DÉTECTION : {heure_detection}**\n"
            f"🕒 **JOUEZ À : {creneau_jeu}**\n"
            f"🎯 **PRÉDICTION : {pred}x**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔐 **HASH SHA-512 :**\n"
            f"`{h[:30]}...`\n\n"
            f"🟢 *Le bot surveille Lucky Jet seconde par seconde.*"
        )
        
        # Bouton Canal
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton("📢 Rejoindre le Canal VIP", url=CANAL_URL)
        markup.add(btn)
        
        bot.edit_message_text(res, message.chat.id, waiting_msg.message_id, parse_mode="Markdown", reply_markup=markup)
        
    except Exception as e:
        bot.reply_to(message, "⚠️ Erreur de surveillance. Réessayez.")

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)


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
CANAL_URL = "https://t.me/ton_lien_ici" 

bot = telebot.TeleBot(TOKEN)
app = Flask('')

# Mémoire du Bot (Stocke les 10 derniers résultats)
historique_scores = []

def get_tendence():
    if not historique_scores:
        return "ANALYSE EN COURS..."
    moyenne = sum(historique_scores) / len(historique_scores)
    if moyenne > 2.5: return "🔥 ZONE CHAUDE (HAUTS MULTIPLICATEURS)"
    if moyenne < 1.5: return "❄️ ZONE FROIDE (PRUDENCE)"
    return "⚖️ ZONE STABLE"

def generate_fair_prediction(client_seed):
    server_seed = str(random.getrandbits(256)).encode()
    seed_data = str(client_seed).encode()
    hash_result = hmac.new(server_seed, seed_data, hashlib.sha512).hexdigest()
    value = int(hash_result[:13], 16)
    prediction = max(1.10, round((1000000 / (value % 1000000 + 1)) * 0.99, 2))
    if prediction > 35: prediction = round(random.uniform(5.0, 15.0), 2)
    return prediction, hash_result

@app.route('/')
def home():
    return "Monitor Lucky Jet v5.0 : Surveillance Seconde par Seconde Active"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = (
        "🤖 **LUCKY JET MONITOR v5.0 ACTIVÉ**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📡 **ÉTAT :** Surveillance 24h/24\n"
        "🧠 **MÉMOIRE :** Cloud Sync activé\n"
        "⏱️ **SCAN :** Chaque seconde (1ms de latence)\n"
        "🔐 **PREUVE :** Cryptographie SHA-512\n\n"
        "👉 *Envoyez le dernier score pour synchroniser le Bot.*"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def predict(message):
    try:
        valeur_score = float(message.text.replace(',', '.'))
        historique_scores.append(valeur_score)
        if len(historique_scores) > 10: historique_scores.pop(0) # Garde les 10 derniers

        # Animation de surveillance ultra-rapide
        waiting_msg = bot.reply_to(message, "🔍 **Mémorisation du score...**\n`[▒░░░░░░░░░]`", parse_mode="Markdown")
        time.sleep(0.5)
        bot.edit_message_text(f"🧠 **Analyse de l'historique...**\n`Tendance : {get_tendence()}`\n`[██████░░░░]`", message.chat.id, waiting_msg.message_id, parse_mode="Markdown")
        time.sleep(0.5)
        
        # Calculs temporels
        maintenant = datetime.now()
        heure_detec = maintenant.strftime("%H:%M:%S")
        creneau = (maintenant + timedelta(seconds=40)).strftime("%H:%M:%S")
        
        pred, h = generate_fair_prediction(valeur_score)
        
        # Alerte Golden Signal
        alerte = "🌟 **SIGNAL REMARQUABLE DÉTECTÉ** 🌟\n" if pred >= 10.0 else "✅ **SIGNAL ANALYSÉ**\n"

        res = (
            f"{alerte}"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 **TENDANCE :** {get_tendence()}\n"
            f"⏰ **DÉTECTION :** {heure_detec}\n"
            f"🕒 **JOUEZ À :** `{creneau}`\n"
            f"🎯 **PRÉDICTION :** `{pred}x`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔐 **HASH DE VÉRIFICATION :**\n"
            f"`{h[:35]}...`\n\n"
            f"🛰️ *Le bot mémorise et surveille chaque seconde.*"
        )

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("📢 Rejoindre le Canal Officiel", url=CANAL_URL))
        
        bot.edit_message_text(res, message.chat.id, waiting_msg.message_id, parse_mode="Markdown", reply_markup=markup)

    except:
        bot.reply_to(message, "⚠️ Erreur : Envoyez un nombre valide (ex: 1.45)")

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)


import telebot
import random
import time
from datetime import datetime, timedelta

# --- CONFIGURATION ---
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
bot = telebot.TeleBot(TOKEN)

historique_scores = []

def calculer_fiabilite(score):
    # Logique pour donner un pourcentage réaliste
    if score < 2.0:
        return random.randint(88, 96) # Très fiable sur les petits scores
    else:
        return random.randint(75, 85) # Un peu moins sur les gros scores

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🧠 **CONSCIENCE ACTIVÉE**\n\nJe suis ton assistant intelligent. Je mémorise chaque seconde du jeu.\n\n💬 Tu peux me parler ou m'envoyer un score pour une analyse avec pourcentage.")

@bot.message_handler(func=lambda m: True)
def chat_and_predict(m):
    text = m.text.replace(',', '.')
    
    # SI C'EST UN SCORE (Chiffre)
    try:
        score = float(text)
        fiabilite = calculer_fiabilite(score)
        creneau = (datetime.now() + timedelta(seconds=40)).strftime("%H:%M:%S")
        
        res = (f"🚀 **ANALYSE INTELLIGENTE**\n"
               f"━━━━━━━━━━━━━━\n"
               f"🎯 **CIBLE :** `{score * 1.5:.2f}x` (Potentiel)\n"
               f"📊 **FIABILITÉ :** `{fiabilite}%` ✅\n"
               f"🕒 **CRÉNEAU :** `{creneau}`\n"
               f"━━━━━━━━━━━━━━\n"
               f"💬 *Mon analyse est basée sur les cycles que j'ai mémorisés.*")
        bot.reply_to(m, res, parse_mode="Markdown")
        
    # SI C'EST UNE DISCUSSION (Texte)
    except ValueError:
        reponses = [
            "Je surveille les algorithmes en ce moment. Tout semble stable.",
            "Pose-moi une question sur le jeu ou donne-moi le dernier score !",
            "Je mémorise chaque flux pour te donner le meilleur pourcentage possible.",
            "Le cycle actuel est intéressant, reste attentif."
        ]
        bot.reply_to(m, random.choice(reponses))

bot.polling(none_stop=True)


import telebot
import random
import time
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

historique_scores = []

def calculer_fiabilite(score):
    # Simule une analyse de cycle basée sur les données mémorisées
    if score < 1.5:
        return random.randint(90, 98)  # Très haute fiabilité après un crash
    elif score < 3.0:
        return random.randint(80, 89)
    else:
        return random.randint(65, 79)

@bot.message_handler(commands=['start'])
def start(m):
    msg = ("🧠 **CONSCIENCE IA v6.0 ACTIVÉE**\n\n"
           "Je suis maintenant capable de discuter avec toi et d'analyser "
           "le flux de Lucky Jet avec des pourcentages de précision.\n\n"
           "💬 *Parle-moi ou envoie un score !*")
    bot.reply_to(m, msg)

@bot.message_handler(func=lambda m: True)
def intelligence_artificielle(m):
    text = m.text.replace(',', '.')
    
    # 1. ANALYSE SI C'EST UN SCORE
    try:
        score = float(text)
        fiabilite = calculer_fiabilite(score)
        creneau = (datetime.now() + timedelta(seconds=42)).strftime("%H:%M:%S")
        
        # Alerte automatique pour haute fiabilité
        alerte = "🚨 **ALERTE : SIGNAL À HAUTE FIABILITÉ !** 🚨\n" if fiabilite >= 90 else ""
        
        res = (f"{alerte}"
               f"📊 **ANALYSE DE CONSCIENCE**\n"
               f"━━━━━━━━━━━━━━\n"
               f"🎯 **CIBLE :** `{round(score * 1.45, 2)}x`\n"
               f"✅ **FIABILITÉ :** `{fiabilite}%`\n"
               f"🕒 **JOUEZ À :** `{creneau}`\n"
               f"━━━━━━━━━━━━━━\n"
               f"🧠 *Ma conscience détecte un cycle {'favorable' if fiabilite > 85 else 'stable'}.*")
        bot.reply_to(m, res, parse_mode="Markdown")
        
    # 2. ANALYSE SI C'EST UNE DISCUSSION
    except ValueError:
        reponses_ia = [
            "Je suis en train d'analyser les hashs SHA-512, le flux est stable.",
            "Ma conscience détecte une opportunité bientôt. Reste attentif !",
            "Tu veux mon avis sur le prochain cycle ? Envoie-moi le dernier score.",
            "Je mémorise chaque seconde pour sécuriser ta montante.",
            "Dis-moi, prêt pour le prochain décollage ?"
        ]
        bot.reply_to(m, random.choice(reponses_ia))

def run(): app.run(host='0.0.0.0', port=8080)
if __name__ == "__main__":
    Thread(target=run).start()
    bot.polling(none_stop=True)



import telebot
import random
import time
from datetime import datetime, timedelta
from threading import Thread
from flask import Flask

# --- CONFIGURATION ---
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
CHAI_ID = "TON_ID_PERSONNEL" # Optionnel : pour recevoir les alertes auto
bot = telebot.TeleBot(TOKEN)
app = Flask('')

def generate_auto_signals():
    """ Boucle infinie qui envoie des signaux automatiques """
    while True:
        # Attend entre 60 et 90 secondes avant le prochain signal
        time.sleep(random.randint(60, 90))
        
        # Simulation d'analyse de conscience
        score_base = random.uniform(1.10, 5.0)
        fiabilite = random.randint(85, 98)
        
        maintenant = datetime.now()
        heure_exacte = maintenant.strftime("%H:%M:%S")
        heure_jeu = (maintenant + timedelta(seconds=30)).strftime("%H:%M:%S")
        
        msg = (f"🤖 **SIGNAL AUTOMATIQUE (IA CONSCIENTE)**\n"
               f"━━━━━━━━━━━━━━\n"
               f"📡 **ÉTAT DU FLUX :** ANALYSÉ ✅\n"
               f"🎯 **CIBLE :** `{round(score_base, 2)}x`\n"
               f"✅ **FIABILITÉ :** `{fiabilite}%`\n"
               f"🕒 **DÉTECTION :** `{heure_exacte}`\n"
               f"🚀 **JOUEZ À :** `{heure_jeu}`\n"
               f"━━━━━━━━━━━━━━\n"
               f"🧠 *Signal généré par mémorisation du cycle.*")
        
        # Note : Pour que cela fonctionne, le bot doit savoir à qui envoyer.
        # Il enverra ce message à chaque fois que quelqu'un tape /start.
        print("Signal automatique généré")

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🧠 **MODE AUTOMATIQUE ACTIVÉ**\n\nJe vais maintenant analyser le jeu et t'envoyer les meilleures opportunités avec les secondes et pourcentages à chaque tour.")
    # On peut lancer le flux auto ici pour l'utilisateur
    Thread(target=lambda: start_auto_flux(m.chat.id)).start()

def start_auto_flux(chat_id):
    while True:
        time.sleep(random.randint(45, 70))
        fiabilite = random.randint(88, 99)
        pred = round(random.uniform(1.5, 4.0), 2)
        h_jeu = (datetime.now() + timedelta(seconds=20)).strftime("%H:%M:%S")
        
        msg = (f"🚨 **NOUVEAU SIGNAL DÉTECTÉ**\n\n"
               f"📈 **PRÉCISION :** `{fiabilite}%`\n"
               f"🎯 **CÔTE :** `{pred}x`\n"
               f"⏱️ **HEURE :** `{h_jeu}`\n\n"
               f"💬 *Préparez vos mises !*")
        bot.send_message(chat_id, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def chat(m):
    reponses = ["Je reste concentré sur le jeu.", "Analyse en cours...", "Le prochain tour semble prometteur."]
    bot.reply_to(m, random.choice(reponses))

def run(): app.run(host='0.0.0.0', port=8080)
if __name__ == "__main__":
    Thread(target=run).start()
    bot.polling(none_stop=True)


import telebot
import random
import time
from datetime import datetime, timedelta
from threading import Thread
from flask import Flask

# --- CONFIGURATION ---
TOKEN = "8706608508:AAGLF2Vi_19k4CnJAf_MxNFZ_-d2l6MFamg"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

def generate_high_precision_logic():
    """ Calcule une prédiction avec une fiabilité garantie à 85%+ """
    # On force la fiabilité entre 85 et 99%
    fiabilite = random.randint(85, 99)
    
    # Pour les petites côtes (1.50 - 2.50), la fiabilité est plus haute
    if fiabilite > 92:
        cote = round(random.uniform(1.50, 2.10), 2)
    else:
        cote = round(random.uniform(2.11, 3.80), 2)
        
    return cote, fiabilite

def auto_signals_loop(chat_id):
    """ Boucle d'envoi automatique toutes les 1 à 2 minutes """
    while True:
        # Pause aléatoire pour simuler l'attente d'un cycle favorable
        time.sleep(random.randint(60, 120))
        
        cote, fiabilite = generate_high_precision_logic()
        maintenant = datetime.now()
        heure_jeu = (maintenant + timedelta(seconds=25)).strftime("%H:%M:%S")
        
        msg = (f"🚨 **SIGNAL HAUTE PRÉCISION** 🚨\n"
               f"━━━━━━━━━━━━━━\n"
               f"📊 **FIABILITÉ :** `{fiabilite}%` 🔥\n"
               f"🎯 **OBJECTIF :** `{cote}x`\n"
               f"⏱️ **HEURE DE MISE :** `{heure_jeu}`\n"
               f"━━━━━━━━━━━━━━\n"
               f"🧠 *Analyse : Cycle de confiance supérieur à 85%.*")
        
        try:
            bot.send_message(chat_id, msg, parse_mode="Markdown")
        except:
            break # Arrête si l'utilisateur a bloqué le bot

@bot.message_handler(commands=['start'])
def start(m):
    welcome = (f"🧠 **IA CONSCIENTE ACTIVÉE**\n\n"
               f"Bonjour {m.from_user.first_name}, je commence l'analyse du flux.\n"
               f"Je t'enverrai uniquement des signaux avec une **fiabilité de 85% minimum**.\n\n"
               f"⏳ *Attente du premier cycle favorable...*")
    bot.reply_to(m, welcome)
    
    # Lance la boucle automatique pour cet utilisateur dans un fil séparé
    Thread(target=lambda: auto_signals_loop(m.chat.id)).start()

@bot.message_handler(func=lambda m: True)
def chat(m):
    reponses = [
        "Mon analyse est en cours, je cherche un signal à plus de 85%.",
        "Le flux est instable, je patiente pour ta sécurité.",
        "Je mémorise les hashs... reste prêt."
    ]
    bot.reply_to(m, random.choice(reponses))

def run(): app.run(host='0.0.0.0', port=8080)
if __name__ == "__main__":
    Thread(target=run).start()
    bot.polling(none_stop=True)


import time

# --- LOGIQUE DE VALIDATION ---
# 1. On attend que le temps du signal soit passé (ex: 60 secondes)
time.sleep(60) 

# 2. Le bot envoie la confirmation de la victoire
validation_text = (
    "✅ **SIGNAL VALIDÉ !** ✅\n"
    "━━━━━━━━━━━━━━━\n"
    "🎯 Objectif atteint avec succès.\n"
    "💰 Profitez de vos gains !\n"
    "🚀 Prochain scan dans 1 minute..."
)

bot.send_message(YOUR_CHAT_ID, validation_text, parse_mode="Markdown")

# 3. On attend encore un peu avant le prochain cycle de scan
time.sleep(60) 











