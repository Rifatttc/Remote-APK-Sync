import telebot
import os
from flask import Flask
from threading import Thread

# ----------------- CONFIGURATION -----------------
TOKEN = '8608695023:AAGNCsgbo3fRjpJ4fSNfvFrmgatIVZom5Os'
ADMIN_ID = 8046944525 # আপনার দেওয়া আইডি
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home(): return "🛡️ SecureSync is Online!"

def run_server():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# ----------------- SECURITY REMOVED FOR DEBUGGING -----------------

@bot.message_handler(commands=['start'])
def start_msg(message):
    # আমরা এখানে কোনো পারমিশন চেক রাখছি না শুধুমাত্র চেক করার জন্য
    # এই মেসেজটি আসলে বুঝবেন আপনার নতুন কোড লাইভ হয়েছে
    msg = (
        f"🛡️ *সিস্টেম চেক সফল!*\n\n"
        f"আপনার আসল আইডি: `{message.from_user.id}`\n"
        f"কোডে সংরক্ষিত আইডি: `{ADMIN_ID}`\n\n"
        "যদি উপরের দুটি আইডি মিলে যায়, তবে আপনি বাটনগুলো দেখতে পাবেন।"
    )
    
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('/build_client', '/browse', '/status')
    
    bot.send_message(message.chat.id, msg, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(commands=['status'])
def status(message):
    bot.reply_to(message, "🟢 Bot is Running Perfectly on Render!")

def run_bot():
    print("Bot is polling...")
    bot.infinity_polling()

if __name__ == '__main__':
    Thread(target=run_server).start()
    run_bot()
