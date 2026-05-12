from telegram import Update

from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

from app.bot.keyboards import MAIN_MENU_KEYBOARD

from app.database.db import SessionLocal

from app.database.queries import (
    get_user_reminders,
    delete_user_reminders,
    count_user_reminders
)


RESET_CONFIRMATION = 100


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user_name = update.effective_user.first_name

    await update.message.reply_text(
        text=(
            f"Hola {user_name} 👋\n\n"
            "Bienvenido a tu bot de recordatorios."
        ),
        reply_markup=MAIN_MENU_KEYBOARD
    )


async def cancel_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        text="Operación cancelada.",
        reply_markup=MAIN_MENU_KEYBOARD
    )


async def show_reminders(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    telegram_id = update.effective_user.id

    session = SessionLocal()

    reminders = get_user_reminders(
        session=session,
        telegram_id=telegram_id
    )

    session.close()

    if not reminders:
        await update.message.reply_text(
            "No tienes citas guardadas."
        )

        return

    message = "📋 Tus citas:\n\n"

    for reminder in reminders:
        formatted_date = reminder.remind_at.strftime(
            "%d/%m/%Y %H:%M"
        )

        message += (
            f"📌 {reminder.title}\n"
            f"⏰ {formatted_date}\n\n"
        )

    await update.message.reply_text(message)


async def start_reset_reminders(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    telegram_id = update.effective_user.id

    session = SessionLocal()

    total = count_user_reminders(
        session=session,
        telegram_id=telegram_id
    )

    session.close()

    if total == 0:
        await update.message.reply_text(
            "No tienes citas para eliminar."
        )

        return ConversationHandler.END

    await update.message.reply_text(
        (
            f"⚠️ Vas a eliminar {total} citas.\n\n"
            "Escribe SI para confirmar."
        )
    )

    return RESET_CONFIRMATION


async def confirm_reset_reminders(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    confirmation = update.message.text.strip().lower()

    if confirmation != "si":
        await update.message.reply_text(
            "Reset cancelado.",
            reply_markup=MAIN_MENU_KEYBOARD
        )

        return ConversationHandler.END

    telegram_id = update.effective_user.id

    session = SessionLocal()

    delete_user_reminders(
        session=session,
        telegram_id=telegram_id
    )

    session.close()

    await update.message.reply_text(
        "✅ Todas tus citas han sido eliminadas.",
        reply_markup=MAIN_MENU_KEYBOARD
    )

    return ConversationHandler.END