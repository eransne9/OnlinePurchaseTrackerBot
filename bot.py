import os
import logging
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# הגדרת לוגים
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    tracking_match = re.search(r'\b([A-Z0-9]{9,20})\b', text)

    if tracking_match:
        tracking_number = tracking_match.group(1)
        response_text = f"נקלט מספר מעקב חדש: {tracking_number}\nמנתח את ההודעה ושומר במערכת..."
    else:
        response_text = "לא זוהה מספר מעקב בהודעה. נסה להעביר הודעת טקסט שמכילה מספר מעקב ברור."

    await update.message.reply_text(response_text)

if __name__ == '__main__':
    if not TOKEN:
        raise ValueError("Missing BOT_TOKEN environment variable!")

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("הבוט מתחיל לפעול...")
    application.run_polling()
