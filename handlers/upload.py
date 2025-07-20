from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ConversationHandler, MessageHandler, CommandHandler, filters, ContextTypes
)
from google.drive import upload_file_to_drive
from core.file_utils import generate_filename

CHOOSING_CLIENT, CHOOSING_OBJECT, CHOOSING_STAGE, CHOOSING_TYPE, CHOOSING_COUNTERPARTY, UPLOADING_FILE = range(6)

user_data = {}

async def start_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выберите клиента:", reply_markup=ReplyKeyboardMarkup([["Client A", "Client B"]], one_time_keyboard=True))
    return CHOOSING_CLIENT

async def choose_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id] = {"client": update.message.text}
    await update.message.reply_text("Выберите объект:")
    return CHOOSING_OBJECT

async def choose_object(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id]["object"] = update.message.text
    await update.message.reply_text("Выберите этап:", reply_markup=ReplyKeyboardMarkup([["Purchase", "Operation"]], one_time_keyboard=True))
    return CHOOSING_STAGE

async def choose_stage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id]["stage"] = update.message.text
    await update.message.reply_text("Тип документа:")
    return CHOOSING_TYPE

async def choose_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id]["type"] = update.message.text
    await update.message.reply_text("Контрагент:")
    return CHOOSING_COUNTERPARTY

async def choose_counterparty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id]["counterparty"] = update.message.text
    await update.message.reply_text("Отправьте файл:")
    return UPLOADING_FILE

async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if not doc:
        await update.message.reply_text("Это не документ. Попробуйте снова.")
        return UPLOADING_FILE

    file = await doc.get_file()
    file_path = await file.download_to_drive()
    data = user_data.get(update.effective_user.id)
    new_name = generate_filename(data)
    gdrive_path = f"{data['client']}/{data['object']}/{data['stage']}"
    drive_link = upload_file_to_drive(file_path, new_name, gdrive_path)

    await update.message.reply_text(f"Файл загружен: {drive_link}")
    return ConversationHandler.END

upload_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("upload", start_upload)],
    states={
        CHOOSING_CLIENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_client)],
        CHOOSING_OBJECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_object)],
        CHOOSING_STAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_stage)],
        CHOOSING_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_type)],
        CHOOSING_COUNTERPARTY: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_counterparty)],
        UPLOADING_FILE: [MessageHandler(filters.Document.ALL, upload_file)],
    },
    fallbacks=[],
)
