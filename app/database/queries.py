from sqlalchemy.orm import Session

from app.database.models import Reminder


def create_reminder(
    session: Session,
    telegram_id: int,
    title: str,
    remind_at
):
    reminder = Reminder(
        telegram_id=telegram_id,
        title=title,
        remind_at=remind_at
    )

    session.add(reminder)
    session.commit()
    session.refresh(reminder)

    return reminder


def get_user_reminders(
    session: Session,
    telegram_id: int
):
    return (
        session.query(Reminder)
        .filter(Reminder.telegram_id == telegram_id)
        .order_by(Reminder.remind_at)
        .all()
    )


def delete_user_reminders(
    session: Session,
    telegram_id: int
):
    reminders = (
        session.query(Reminder)
        .filter(Reminder.telegram_id == telegram_id)
        .all()
    )

    for reminder in reminders:
        session.delete(reminder)

    session.commit()


def count_user_reminders(
    session: Session,
    telegram_id: int
):
    return (
        session.query(Reminder)
        .filter(Reminder.telegram_id == telegram_id)
        .count()
    )


def delete_reminder_by_id(
    session: Session,
    reminder_id: int
):
    reminder = (
        session.query(Reminder)
        .filter(Reminder.id == reminder_id)
        .first()
    )

    if reminder:
        session.delete(reminder)
        session.commit()


def get_all_reminders(
    session: Session
):
    return session.query(Reminder).all()