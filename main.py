import os
import random
import asyncio
import threading
from flask import Flask
from telegram import Update, ReactionTypeEmoji
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running perfectly!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

BOT_TOKEN = os.getenv("BOT_TOKEN")
UNIQUE_EMOJIS = [
    "👍", "👎", "❤️", "🔥", "🥰", "👏", "😁", "🤔", 
    "🤯", "😱", "🤬", "😢", "🎉", "🤩", "🤮", "💩", 
    "🙏", "👌", "🕊", "🤡", "🥱", "🥴", "😍", "🐳", "❤️‍🔥"
]

# ব্যাকগ্রাউন্ড প্রসেসিং টাস্ক (যাতে কোনো মেসেজ ব্লক না হয়)
async def process_reaction(bot, chat_id, message_id):
    try:
        selected_emoji = random.choice(UNIQUE_EMOJIS)
        await bot.set_message_reaction(
            chat_id=chat_id,
            message_id=message_id,
            reaction=[ReactionTypeEmoji(emoji=selected_emoji)]
        )
    except Exception as e:
        print(f"Reaction Error: {e}")

async def auto_react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat and update.effective_message:
        chat_id = update.effective_chat.id
        message_id = update.effective_message.message_id
        
        # মূল থ্রেড না থামিয়ে ব্যাকগ্রাউন্ডে রিঅ্যাকশন প্রসেস করা (মিলি-সেকেন্ড হ্যান্ডলিং)
        asyncio.create_task(process_reaction(context.bot, chat_id, message_id))

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN is missing!")
        exit(1)

    threading.Thread(target=run_flask, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, auto_react))

    print("Bot is starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
