import os
import random
import threading
from flask import Flask
from telegram import Update, ReactionTypeEmoji
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Render Free Web Service-এর জন্য ফেক ওয়েব সার্ভার তৈরি (Port Error এড়াতে)
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running perfectly!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

# Bot API Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# আপনার দেওয়া ইউনিক ইমোজির তালিকা (এখান থেকে প্রতিবার যেকোনো একটি বেছে নেওয়া হবে)
UNIQUE_EMOJIS = ["⚡", "👑", "🎯", "🦋", "🏆", "✨", "🔥", "❤️", "🎉", "🦄"]

async def auto_react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.effective_chat.id
        message_id = update.effective_message.message_id

        # তালিকা থেকে র‍্যান্ডমভাবে একটি ইমোজি পছন্দ করা
        selected_emoji = random.choice(UNIQUE_EMOJIS)

        # মেসেজে নির্বাচিত ইমোজিটি রিঅ্যাক্ট করা
        await context.bot.set_message_reaction(
            chat_id=chat_id,
            message_id=message_id,
            reaction=[ReactionTypeEmoji(emoji=selected_emoji)]
        )
        print(f"Reacted with {selected_emoji} to message {message_id}")
    except Exception as e:
        print(f"Reaction Error: {e}")

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN Environment Variable is missing!")
        exit(1)

    # ব্যাকগ্রাউন্ডে ফ্ল্যাস্ক ওয়েবসাইট চালু করা
    threading.Thread(target=run_flask, daemon=True).start()

    # টেলিগ্রাম বট স্টার্ট করা
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, auto_react))

    print("Bot is starting...")
    app.run_polling(drop_pending_updates=True)
