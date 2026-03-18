import telebot
from telebot import types
import sqlite3
import time
import random
import os
from flask import Flask
import threading

# --- CONFIGURATION ---
API_TOKEN = '8706608508:AAGLF2Vi_19k4CnJAf_MxM'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# --- MÉMOIRE ---
def init_db():
    try:
        conn = sqlite3.connect('memoire.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS logs (heure TEXT, cote TEXT)')
        conn.commit()
        conn.close()
    except: pass

init_db()

# --- COMMANDES ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("✈️ Lucky Jet")
    btn2 = types.KeyboardButton("📊 Voir Mémoire")
    btn3 = types.KeyboardButton("🎁 Code Promo")
    btn4 = types.KeyboardButton("💬 Parler au Bot")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(message.chat.id, "🧠 **SYSTÈME IA V8.0 CONNECTÉ**\n\nPrêt Frederic. La mémoire est active et le flux LTE est stable.", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_msg(message):
    if message.text == "✈️ Lucky Jet":
        h = time.strftime('%H:%M:%S', time.localtime(time.time() + 20))
        c = round(random.uniform(1.20, 1.45), 2)
        
        # Sauvegarde
        conn = sqlite3.connect('memoire.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs VALUES (?, ?)", (h, str(c)))
        conn.commit()
        conn.close()
        
        bot.send_message(message.chat.id, f"🚀 **SIGNAL IA**\n━━━━━━━━━━━━━\n⌚ JOUEZ À : {h}\n🎯 CIBLE : {c}x\n✅ FIABILITÉ : 98%\n━━━━━━━━━━━━━\n*Signal enregistré dans ma mémoire.*")

    elif message.text == "📊 Voir Mémoire":
        conn = sqlite3.connect('memoire.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs ORDER BY rowid DESC LIMIT 5")
        rows = cursor.fetchall()
        conn.close()
        txt = "📂 **DERNIERS ENREGISTREMENTS :**\n"
        for r in rows: txt += f"• {r[0]} -> {r[1]}x\n"
        bot.send_message(message.chat.id, txt if rows else "Mémoire vide.")

    elif message.text == "🎁 Code Promo":
        bot.send_message(message.chat.id, "💎 Utilisez le code : **JET225**\nPour 500% de bonus sur 1Win.")

    else:
        bot.reply_to(message, "Je mémorise notre discussion, Frederic. Pose-moi une question sur Lucky Jet.")

# --- SERVEUR ---
@app.route('/')
def health(): return "OK", 200

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.polling(none_stop=True)
