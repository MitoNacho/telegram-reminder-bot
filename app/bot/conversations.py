from datetime import datetime

from telegram import Update

from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

from app.bot.keyboards import (
    MAIN_MENU_KEYBOARD,
    CANCEL_BUTTON
)

from app.bot.states import (
    TITLE,
    DATE,
    TIME,
    CONFIRM
)

from app.database.db import SessionLocal
from app.database.queries import create_reminder

from app.scheduler.reminder_scheduler import schedule_reminder


async def start_add_reminder(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    context.user_data.clear()

    await update.message.reply_text(
        "📝 Escribe el asunto del recordatorio:"
    )

    return TITLE


async def receive_title(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    title = update.message.text.strip()

    # Cancelar conversación
    if title == CANCEL_BUTTON:
        return await cancel_conversation(update, context)

    # Validar vacío
    if not title:
        await update.message.reply_text(
            "El asunto no puede estar vacío."
        )

        return TITLE

    context.user_data["title"] = title

    await update.message.reply_text(
        "📅 Escribe la fecha.\n\n"
        "Formato: DD/MM/YYYY"
    )

    return DATE


async def receive_date(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    date_text = update.message.text.strip()

    if date_text == CANCEL_BUTTON:
        return await cancel_conversation(update, context)

    try:
        parsed_date = datetime.strptime(
            date_text,
            "%d/%m/%Y"
        )

        # Validar fecha pasada
        if parsed_date.date() < datetime.now().date():

            await update.message.reply_text(
                "No puedes usar fechas pasadas."
            )

            return DATE

        context.user_data["date"] = parsed_date

        await update.message.reply_text(
            "⏰ Escribe la hora.\n\n"
            "Formato: HH:MM"
        )

        return TIME

    except ValueError:

        await update.message.reply_text(
            "❌ Fecha inválida.\n"
            "Usa formato DD/MM/YYYY"
        )

        return DATE


async def receive_time(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    time_text = update.message.text.strip()

    if time_text == CANCEL_BUTTON:
        return await cancel_conversation(update, context)

    try:
        parsed_time = datetime.strptime(
            time_text,
            "%H:%M"
        ).time()

        stored_date = context.user_data["date"]

        final_datetime = datetime.combine(
            stored_date.date(),
            parsed_time
        )

        # Validar datetime pasado
        if final_datetime < datetime.now():

            await update.message.reply_text(
                "No puedes crear recordatorios en el pasado."
            )

            return TIME

        context.user_data["final_datetime"] = final_datetime

        title = context.user_data["title"]

        await update.message.reply_text(
            (
                f"📌 Confirma el recordatorio:\n\n"
                f"Asunto: {title}\n"
                f"Fecha: {final_datetime.strftime('%d/%m/%Y %H:%M')}\n\n"
                f"Escribe SI para confirmar."
            )
        )

        return CONFIRM

    except ValueError:

        await update.message.reply_text(
            "❌ Hora inválida.\n"
            "Usa formato HH:MM"
        )

        return TIME


async def confirm_reminder(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    confirmation = update.message.text.strip().lower()

    if confirmation == CANCEL_BUTTON.lower():
        return await cancel_conversation(update, context)

    if confirmation != "si":

        await update.message.reply_text(
            "Creación cancelada.",
            reply_markup=MAIN_MENU_KEYBOARD
        )

        context.user_data.clear()

        return ConversationHandler.END

    telegram_id = update.effective_user.id

    title = context.user_data["title"]

    remind_at = context.user_data["final_datetime"]

    session = SessionLocal()

    reminder = create_reminder(
        session=session,
        telegram_id=telegram_id,
        title=title,
        remind_at=remind_at
    )

    schedule_reminder(
        bot=context.bot,
        reminder=reminder
    )

    session.close()

    await update.message.reply_text(
        (
            "✅ Recordatorio creado correctamente.\n\n"
            f"📌 {title}\n"
            f"⏰ {remind_at.strftime('%d/%m/%Y %H:%M')}"
        ),
        reply_markup=MAIN_MENU_KEYBOARD
    )

    context.user_data.clear()

    return ConversationHandler.END


async def cancel_conversation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    context.user_data.clear()

    await update.message.reply_text(
        "❌ Operación cancelada.",
        reply_markup=MAIN_MENU_KEYBOARD
    )

    return ConversationHandler.END