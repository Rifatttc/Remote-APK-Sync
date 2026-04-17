# এটি আপনার cdfile.py এর জন্য আরও শক্তিশালী আনলক কোড
import telebot
import os
from telebot import types
from flask import Flask
from threading import Thread

TOKEN = '8608695023:AAGNCsgbo3fRjpJ4fSNfvFrmgatIVZom5Os'
# আপনার আইডি স্ট্রিং এবং ইন্টিজার দুই ভাবেই চেক করবে যাতে কোনো এরর না হয়
ADMIN_ID = 8046944525 

bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home(): return "Bot is Alive!"

def run_server():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# একদম কড়া সিকিউরিটি চেক
def is_admin(m):
    return m.from_user.id == ADMIN_ID or str(m.chat.id) == str(ADMIN_ID)

@bot.message_handler(commands=['start'])
def start_msg(message):
    print(f"DEBUG: User connected with ID: {message.from_user.id}") # রেন্ডার লগে আইডি দেখার জন্য
    if not is_admin(message):
        bot.reply_to(message, f"🚫 Access Denied.\nYour ID: `{message.from_user.id}` is not whitelisted.", parse_mode='Markdown')
        return

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('/build_client', '/browse', '/status')
    bot.send_message(message.chat.id, "🛡️ স্বাগতম এডমিন! হার্ডওয়্যার আনলক সফল।", reply_markup=markup)

@bot.message_handler(commands=['status'])
def status(message):
    if is_admin(message): bot.reply_to(message, "🟢 Bot is Online on Render!")

# -----------------
def run_bot(): bot.infinity_polling()

if __name__ == '__main__':
    Thread(target=run_server).start()
    run_bot()
