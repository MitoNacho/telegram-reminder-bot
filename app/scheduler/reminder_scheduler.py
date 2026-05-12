from datetime import datetime
from datetime import timedelta

import pytz

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.database.db import SessionLocal

from app.database.queries import (
    delete_reminder_by_id,
    get_all_reminders
)


# Timezone España
SPAIN_TZ = pytz.timezone("Europe/Madrid")


scheduler = AsyncIOScheduler(
    timezone=SPAIN_TZ
)


def start_scheduler():

    if not scheduler.running:

        scheduler.start()

        print("✅ Scheduler iniciado")


async def send_reminder(
    bot,
    reminder_id: int,
    telegram_id: int,
    title: str,
    reminder_type: str
):
    try:

        # Reminder 1 hora antes
        if reminder_type == "before":

            message = (
                f"⏰ Recordatorio en 1 hora:\n\n"
                f"📌 {title}"
            )

        # Reminder exacto
        else:

            message = (
                f"🚨 Recordatorio:\n\n"
                f"📌 {title}"
            )

        # Enviar mensaje Telegram
        await bot.send_message(
            chat_id=telegram_id,
            text=message
        )

        print(
            f"✅ Reminder enviado -> {title}"
        )

        # 🔥 BORRAR cita tras reminder exacto
        if reminder_type == "exact":

            session = SessionLocal()

            delete_reminder_by_id(
                session=session,
                reminder_id=reminder_id
            )

            session.close()

            print(
                f"🗑️ Reminder eliminado -> {title}"
            )

    except Exception as error:

        print(
            f"❌ Error enviando reminder: {error}"
        )


def schedule_reminder(
    bot,
    reminder
):
    try:

        reminder_datetime = reminder.remind_at

        # Añadir timezone si no existe
        if reminder_datetime.tzinfo is None:

            reminder_datetime = SPAIN_TZ.localize(
                reminder_datetime
            )

        one_hour_before = (
            reminder_datetime - timedelta(hours=1)
        )

        now = datetime.now(SPAIN_TZ)

        print("==========")
        print("NOW:", now)
        print("REMINDER:", reminder_datetime)
        print("1 HOUR BEFORE:", one_hour_before)
        print("==========")

        # JOB 1 hora antes
        if one_hour_before > now:

            scheduler.add_job(
                send_reminder,
                trigger="date",
                run_date=one_hour_before,
                args=[
                    bot,
                    reminder.id,
                    reminder.telegram_id,
                    reminder.title,
                    "before"
                ],
                id=f"before_{reminder.id}",
                replace_existing=True
            )

            print(
                f"✅ BEFORE JOB creado -> {reminder.title}"
            )

        # JOB exacto
        if reminder_datetime > now:

            scheduler.add_job(
                send_reminder,
                trigger="date",
                run_date=reminder_datetime,
                args=[
                    bot,
                    reminder.id,
                    reminder.telegram_id,
                    reminder.title,
                    "exact"
                ],
                id=f"exact_{reminder.id}",
                replace_existing=True
            )

            print(
                f"✅ EXACT JOB creado -> {reminder.title}"
            )

    except Exception as error:

        print(
            f"❌ Error creando scheduler job: {error}"
        )


def restore_scheduler_jobs(
    bot
):
    try:

        session = SessionLocal()

        reminders = get_all_reminders(
            session=session
        )

        session.close()

        print(
            f"🔄 Restaurando {len(reminders)} reminders"
        )

        for reminder in reminders:

            schedule_reminder(
                bot=bot,
                reminder=reminder
            )

        print(
            "✅ Restauración completada"
        )

    except Exception as error:

        print(
            f"❌ Error restaurando jobs: {error}"
        )