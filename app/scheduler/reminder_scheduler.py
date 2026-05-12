from datetime import datetime
from datetime import timedelta

import pytz

from apscheduler.schedulers.asyncio import AsyncIOScheduler


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
    chat_id: int,
    title: str,
    reminder_type: str
):
    try:

        if reminder_type == "before":

            message = (
                f"⏰ Recordatorio en 1 hora:\n\n"
                f"📌 {title}"
            )

        else:

            message = (
                f"🚨 Recordatorio:\n\n"
                f"📌 {title}"
            )

        await bot.send_message(
            chat_id=chat_id,
            text=message
        )

        print(
            f"✅ Reminder enviado -> {title}"
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

        # Convertir a timezone España
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

        # Reminder 1h antes
        if one_hour_before > now:

            scheduler.add_job(
                send_reminder,
                trigger="date",
                run_date=one_hour_before,
                args=[
                    bot,
                    reminder.telegram_id,
                    reminder.title,
                    "before"
                ],
                id=f"before_{reminder.id}",
                replace_existing=True
            )

            print(
                f"✅ Job BEFORE creado -> {reminder.title}"
            )

        # Reminder exacto
        if reminder_datetime > now:

            scheduler.add_job(
                send_reminder,
                trigger="date",
                run_date=reminder_datetime,
                args=[
                    bot,
                    reminder.telegram_id,
                    reminder.title,
                    "exact"
                ],
                id=f"exact_{reminder.id}",
                replace_existing=True
            )

            print(
                f"✅ Job EXACT creado -> {reminder.title}"
            )

    except Exception as error:

        print(
            f"❌ Error creando scheduler job: {error}"
        )