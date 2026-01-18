import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from groq import Groq  # <-- Используем родную библиотеку Groq

# --- ТВОИ КЛЮЧИ ---
MY_TELEGRAM_TOKEN = "8439792492:AAHRPCJt62NHXGtdteyffjZY-0vRBCw0GqM"
GROQ_API_KEY = "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"
# ------------------

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Создаем клиент Groq напрямую
client = Groq(
    api_key=GROQ_API_KEY,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Я працюю через офіційну бібліотеку Groq (Llama 3.3). Питайте!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id
    
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        chat_completion = client.chat.completions.create(
            # Самая новая и рабочая модель на сегодня:
            model="llama-3.3-70b-versatile",
            
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant. Always answer in the same language as the user's message."
                },
                {
                    "role": "user", 
                    "content": user_text
                }
            ]
        )
        
        answer = chat_completion.choices[0].message.content
        await update.message.reply_text(answer)

    except Exception as e:
        print(f"ОШИБКА: {e}")
        await update.message.reply_text(f"Error: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(MY_TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот Groq Official запущен!")
    app.run_polling()