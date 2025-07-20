from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
)
from google.sheet import get_allowed_objects, get_vendor_credentials

CHOOSING_CLIENT, CHOOSING_OBJECT, CHOOSING_VENDOR = range(3)
user_data = {}

async def start_credentials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    allowed = get_allowed_objects(user_id)
    if not allowed:
        await update.message.reply_text("У вас нет доступа к объектам.")
        return ConversationHandler.END

    clients = sorted(set(row["client"] for row in allowed))
    context.user_data["allowed"] = allowed

    await update.message.reply_text(
        "Выберите клиента:",
        reply_markup=ReplyKeyboardMarkup([[c] for c in clients], one_time_keyboard=True, resize_keyboard=True)
    )
    return CHOOSING_CLIENT

async def choose_client(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client = update.message.text
    context.user_data["client"] = client
    objects = [row["object"] for row in context.user_data["allowed"] if row["client"] == client]

    await update.message.reply_text(
        "Выберите объект:",
        reply_markup=ReplyKeyboardMarkup([[o] for o in sorted(set(objects))], one_time_keyboard=True, resize_keyboard=True)
    )
    return CHOOSING_OBJECT

async def choose_object(update: Update, context: ContextTypes.DEFAULT_TYPE):
    obj = update.message.text
    context.user_data["object"] = obj
    creds = get_vendor_credentials(context.user_data["client"], obj)

    if not creds:
        await update.message.reply_text("Нет данных по вендорам для этого объекта.")
        return ConversationHandler.END

    context.user_data["creds"] = creds
    vendors = [row["vendor_name"] for row in creds]

    await update.message.reply_text(
        "Выберите вендора:",
        reply_markup=ReplyKeyboardMarkup([[v] for v in vendors], one_time_keyboard=True, resize_keyboard=True)
    )
    return CHOOSING_VENDOR

async def choose_vendor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    vendor_name = update.message.text
    cred = next((row for row in context.user_data["creds"] if row["vendor_name"] == vendor_name), None)

    if not cred:
        await update.message.reply_text("Ошибка: вендор не найден.")
        return ConversationHandler.END

    msg = (
        f"🔐 <b>{vendor_name}</b>\n"
        f"🌐 <a href='{cred['url']}'>{cred['url']}</a>\n"
        f"👤 <code>{cred['login']}</code>\n"
        f"🔑 <code>{cred['password']}</code>"
    )
    await update.message.reply_text(msg, parse_mode="HTML", disable_web_page_preview=True)
    return ConversationHandler.END

credentials_handler = ConversationHandler(
    entry_points=[CommandHandler("credentials", start_credentials)],
    states={
        CHOOSING_CLIENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_client)],
        CHOOSING_OBJECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_object)],
        CHOOSING_VENDOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_vendor)],
    },
    fallbacks=[],
)
