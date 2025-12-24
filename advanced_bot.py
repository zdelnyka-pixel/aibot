# bot.py — безопасный Telegram-бот с нейросетью
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq

# Получаем ключи из переменных окружения
TELEGRAM_TOKEN = ""
GROQ_API_KEY = ""

if not TELEGRAM_TOKEN:
    raise RuntimeError("❌ Не задан TELEGRAM_TOKEN. Установите его как переменную окружения.")
if not GROQ_API_KEY:
    raise RuntimeError("❌ Не задан GROQ_API_KEY. Установите его как переменную окружения.")

client = Groq(api_key=GROQ_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я — ИИ-бот на базе Llama 3. "
        "Напишите любой вопрос, и я постараюсь помочь!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        await update.message.reply_text("🤔 Думаю...")
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_text}],
            model="llama-3.1-8b-instant",
        )
        answer = chat_completion.choices[0].message.content
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text("⚠️ Извините, что-то пошло не так. Попробуйте позже.")
        print("Ошибка:", e)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Бот запущен! Готов отвечать на сообщения...")
    app.run_polling()

if __name__ == "__main__":
    main()