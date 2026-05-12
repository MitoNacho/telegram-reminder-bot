from datetime import timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()


def start_scheduler():
    scheduler.start()


async def send_reminder(
    bot,
    chat_id: int,
    title: str,
    reminder_type: str
):
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


def schedule_reminder(
    bot,
    reminder
):
    reminder_datetime = reminder.remind_at

    one_hour_before = (
        reminder_datetime - timedelta(hours=1)
    )

    # Recordatorio 1 hora antes
    from datetime import datetime

    if one_hour_before > datetime.now():
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
            id=f"before_{reminder.id}"
        )

    # Recordatorio exacto
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
        id=f"exact_{reminder.id}"
    )