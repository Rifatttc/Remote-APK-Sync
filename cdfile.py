import telebot
import os
from telebot import types
from flask import Flask
from threading import Thread

# ----------------- CONFIGURATION -----------------
TOKEN = '8608695023:AAGNCsgbo3fRjpJ4fSNfvFrmgatIVZom5Os'
ADMIN_ID = 8046944525  # আপনার আইডি নিশ্চিত করা হয়েছে
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running"

def run_server():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# ----------------- SECURITY CHECK -----------------
def is_admin(user_id):
    # স্ট্রিং হিসেবে তুলনা করা সবথেকে নিরাপদ, এতে এরর হবে না
    return str(user_id) == str(ADMIN_ID)

# ----------------- BOT LOGIC -----------------

@bot.message_handler(func=lambda message: not is_admin(message.from_user.id))
def unauthorized(message):
    current_id = message.from_user.id
    # যদি এরপরও এক্সেস না পান, বট আপনাকে মেসেজে বলবে সে আপনার কোন আইডি দেখছে
    bot.reply_to(message, f"🚫 *Access Denied.*\n\nসিস্টেম আপনাকে অনুমতি দিচ্ছে না।\nআপনার আইডি: `{current_id}`\nকোডে সেট করা আইডি: `{ADMIN_ID}`\n\nযদি আপনার আইডি ভিন্ন হয়, তবে ওই আইডিটি আমাকে দিন।", parse_mode='Markdown')

@bot.message_handler(commands=['start'])
def start_msg(message):
    if not is_admin(message.from_user.id):
        unauthorized(message)
        return
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('/build_client')
    btn2 = types.KeyboardButton('/browse')
    btn3 = types.KeyboardButton('/status')
    markup.add(btn1, btn2, btn3)
    
    welcome = (
        "🛡️ *SecureSync Remote Management* 🛡️\n\n"
        "স্বাগতম এডমিন! এবার সিস্টেম আনলক হওয়ার কথা।\n"
        "নিচের কমান্ডগুলো ব্যবহার করুন:\n\n"
        "🚀 /build_client - ক্লায়েন্ট স্ক্রিপ্ট জেনারেট করুন।\n"
        "📁 /browse - স্টোরেজ ফাইল ব্রাউজ করুন।\n"
        "📊 /status - সিস্টেম চেক।"
    )
    bot.send_message(message.chat.id, welcome, parse_mode='Markdown', reply_markup=markup)

# ... বাকি কোড (browse, build_client) নিচে আগের মতোই থাকবে।

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    t = Thread(target=run_server)
    t.start()
    run_bot()
