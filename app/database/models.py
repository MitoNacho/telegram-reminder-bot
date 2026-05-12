from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.db import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)

    telegram_id = Column(
        BigInteger,
        nullable=False,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    remind_at = Column(
        DateTime,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )