from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
)
from google.sheet import get_allowed_objects
from google.drive import list_files_in_folder_path

CHOOSING_CLIENT, CHOOSING_OBJECT, CHOOSING_STAGE = range(3)

async def start_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    allowed = get_allowed_objects(user_id)
    if not allowed:
        await update.message.reply_text("У вас нет доступа к объектам.")
        return ConversationHandler.END

    clients = sorted(set(row["client"] for row in allowed))
    context.user_data["allowed"] = allowed

    await update.message.reply_text(
        "Выберите клиента:",
        reply_markup=ReplyKeyboardMarkup([[c] for c in clients], one_time_keyboard=True)
    )
    return CHOOSING_CLIENT

async def choose_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client = update.message.text
    context.user_data["client"] = client
    objects = [row["object"] for row in context.user_data["allowed"] if row["client"] == client]
    await update.message.reply_text(
        "Выберите объект:",
        reply_markup=ReplyKeyboardMarkup([[o] for o in sorted(set(objects))], one_time_keyboard=True)
    )
    return CHOOSING_OBJECT

async def choose_object(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["object"] = update.message.text
    await update.message.reply_text(
        "Выберите этап:",
        reply_markup=ReplyKeyboardMarkup([["Purchase", "Operation"]], one_time_keyboard=True)
    )
    return CHOOSING_STAGE

async def choose_stage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["stage"] = update.message.text
    folder_path = f"{context.user_data['client']}/{context.user_data['object']}/{context.user_data['stage']}"
    files = list_files_in_folder_path(folder_path)

    if not files:
        await update.message.reply_text("Файлы не найдены.")
    else:
        msg = "\n\n".join([f"📄 {f['name']}\n🔗 {f['link']}" for f in files])
        await update.message.reply_text(msg)

    return ConversationHandler.END

view_files_handler = ConversationHandler(
    entry_points=[CommandHandler("view", start_view)],
    states={
        CHOOSING_CLIENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_client)],
        CHOOSING_OBJECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_object)],
        CHOOSING_STAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_stage)],
    },
    fallbacks=[],
)
