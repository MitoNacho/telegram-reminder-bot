import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
<<<<<<< HEAD

DATABASE_URL = os.getenv("DATABASE_URL")

# 🔥 FIX IMPORTANTE PARA EVITAR psycopg2
if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql+psycopg://",
            1
        )

    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1
        )
=======
DATABASE_URL = os.getenv("DATABASE_URL")

# FIX RAILWAY + SQLALCHEMY + PSYCOPG3
if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)

    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
>>>>>>> aa583fe (fix railway db driver)
