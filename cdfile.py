import telebot
import os
from telebot import types
from flask import Flask
from threading import Thread

# ----------------- CONFIGURATION -----------------
TOKEN = '8608695023:AAGNCsgbo3fRjpJ4fSNfvFrmgatIVZom5Os'
ADMIN_ID = 8046944525  # আপনার আইডি সেট করা হয়েছে
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "🛡️ SecureSync Server is Live!"

def run_server():
    # Render-এর পোর্টের সাথে মিল রাখা
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# ----------------- SECURITY CHECK -----------------
def is_admin(user_id):
    return user_id == ADMIN_ID

# ----------------- BOT LOGIC -----------------

@bot.message_handler(func=lambda message: not is_admin(message.from_user.id))
def unauthorized(message):
    bot.reply_to(message, "🚫 *Access Denied.*\nThis is a private management tool.", parse_mode='Markdown')

@bot.message_handler(commands=['start'])
def start_msg(message):
    if not is_admin(message.from_user.id): return
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('/build_client')
    btn2 = types.KeyboardButton('/browse')
    btn3 = types.KeyboardButton('/status')
    markup.add(btn1, btn2, btn3)
    
    welcome = (
        "🛡️ *SecureSync Remote Management* 🛡️\n\n"
        "স্বাগতম এডমিন! সিস্টেম আপনার জন্য আনলক করা হয়েছে।\n"
        "নিচের কমান্ডগুলো ব্যবহার করুন:\n\n"
        "🚀 /build_client - ক্লায়েন্ট স্ক্রিপ্ট জেনারেট করুন।\n"
        "📁 /browse - স্টোরেজ ফাইল ব্রাউজ করুন।\n"
        "📊 /status - সিস্টেম চেক।"
    )
    bot.send_message(message.chat.id, welcome, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(commands=['status'])
def status(message):
    if not is_admin(message.from_user.id): return
    bot.reply_to(message, "🟢 *Status:* Online (Render Hub)")

# ----------------- KEEP ALIVE -----------------

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    # সার্ভার এবং বট একসাথে চালানো
    t = Thread(target=run_server)
    t.start()
    run_bot()
