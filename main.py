import os
from telegram import Update, ReactionTypeEmoji
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Render-এর Environment Variable থেকে টোকেন নেওয়া হবে
BOT_TOKEN = os.getenv("BOT_TOKEN")

# আপনার দেওয়া ৬টি ইউনিক ইমোজি
CUSTOM_EMOJIS = ["⚡", "👑", "🎯", "🦋", "🏆", "✨"]

async def auto_react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.effective_chat.id
        message_id = update.effective_message.message_id

        # Telegram Reaction Object তৈরি
        reactions = [ReactionTypeEmoji(emoji=e) for e in CUSTOM_EMOJIS]

        # মেসেজে অটো ইমোজি রিঅ্যাকশন দেওয়া
        await context.bot.set_message_reaction(
            chat_id=chat_id,
            message_id=message_id,
            reaction=reactions,
            is_big=False
        )
    except Exception as e:
        print(f"Error setting reaction: {e}")

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN Environment Variable is missing!")
        exit(1)

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # চ্যানেল এবং গ্রুপে পোস্ট হলেই রিয়্যাক্ট করবে
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, auto_react))

    print("Bot is running...")
    app.run_polling(drop_pending_updates=True)
