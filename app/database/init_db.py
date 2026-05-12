from app.database.db import Base
from app.database.db import engine

from app.database.models import Reminder


def init_db():
    Base.metadata.create_all(bind=engine)

init_db()