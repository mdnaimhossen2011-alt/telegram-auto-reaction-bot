import os
import random
import asyncio
import threading
from flask import Flask
from telegram import Update, ReactionTypeEmoji
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Render Free Web Service-এর জন্য ফেক ওয়েব সার্ভার (Port Error এড়াতে)
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running perfectly!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

# Bot API Token (Render Environment Variables থেকে নেওয়া হবে)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# আপনার পছন্দের ইউনিক ইমোজির তালিকা
UNIQUE_EMOJIS = ["⚡", "👑", "🎯", "🦋", "🏆", "✨", "🔥", "🎉", "🦄"]

async def auto_react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # মেসেজ পাওয়ার পর ১ সেকেন্ড পজ (টেলিগ্রামের রেট লিমিট এড়ানোর জন্য)
        await asyncio.sleep(1)

        chat_id = update.effective_chat.id
        message_id = update.effective_message.message_id

        # ইমোজি লিস্ট থেকে র‍্যান্ডম একটি সিলেক্ট করা
        selected_emoji = random.choice(UNIQUE_EMOJIS)

        # রিঅ্যাকশন সেন্ড করা
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

    # ইউজারদের কমান্ডসহ সব টেক্সট ও আপডেট ক্যাপচার করার ফিল্টার
    app.add_handler(MessageHandler(filters.ALL, auto_react))

    print("Bot is starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
