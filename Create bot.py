import os
import logging
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")

def get_tracking_info(tracking_number):
    # זיהוי חברת שילוח לפי מבנה המספר
    if tracking_number.startswith("RR") or tracking_number.startswith("EE") or tracking_number.startswith("CP"):
        carrier = "דואר ישראל"
        tracking_url = f"https://www.israelpost.co.il/itemtrace.nsf/mainsearch?OpenForm&itemcode={tracking_number}"
    elif len(tracking_number) >= 12 and tracking_number.isdigit():
        carrier = "אליאקספרס / Cainiao"
        tracking_url = f"https://global.cainiao.com/detail.htm?mailNoList={tracking_number}"
    else:
        carrier = "מעקב בינלאומי (17track)"
        tracking_url = f"https://www.17track.net/en/track?nums={tracking_number}"
        
    return carrier, tracking_url

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    tracking_match = re.search(r'\b([A-Z0-9]{9,20})\b', text)
    
    if tracking_match:
        tracking_number = tracking_match.group(1)
        carrier, tracking_url = get_tracking_info(tracking_number)
        
        response_text = (
            f"📦 **זוהה מספר מעקב:** `{tracking_number}`\n"
            f"🏢 **חברה משוערת:** {carrier}\n\n"
            f"🔗 [לחץ כאן למעקב ישיר באתר]({tracking_url})"
        )
    else:
        response_text = "לא זוהה מספר מעקב בהודעה. נסה לשלוח מספר מעקב תקין."

    await update.message.reply_text(response_text, parse_mode="Markdown")

if __name__ == '__main__':
    if not TOKEN:
        raise ValueError("Missing BOT_TOKEN environment variable!")
    
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("הבוט מתחיל לפעול עם זיהוי מעקב...")
    application.run_polling()
