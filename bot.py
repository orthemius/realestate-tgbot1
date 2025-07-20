import logging
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes
)
from dotenv import load_dotenv

# Импорты твоих обработчиков
from handlers.upload import upload_conversation_handler
from handlers.credentials import credentials_handler
from handlers.view_files import view_files_handler

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

MAIN_MENU = ReplyKeyboardMarkup(
    [["📤 Загрузить файл", "📁 Посмотреть файлы"],
     ["🔐 Логины и пароли", "⚙️ Настройки"]],
    resize_keyboard=True
)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать в RealEstateBot 👋", reply_markup=MAIN_MENU)

# Обработка кликов по кнопкам
async def main_menu_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📤 Загрузить файл":
        return await update.message.reply_text("Введите /upload чтобы загрузить файл.")
    elif text == "📁 Посмотреть файлы":
        return await update.message.reply_text("Введите /view чтобы отфильтровать документы.")
    elif text == "🔐 Логины и пароли":
        return await update.message.reply_text("Введите /credentials для доступа к учёткам.")
    elif text == "⚙️ Настройки":
        return await update.message.reply_text("Настройки пока не реализованы.")
    else:
        return await update.message.reply_text("Выберите действие через меню ниже.")

# Главная функция запуска
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(upload_conversation_handler)
    app.add_handler(credentials_handler)
    app.add_handler(view_files_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_router))

    app.run_polling()

if __name__ == "__main__":
    main()
