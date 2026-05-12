from telegram import ReplyKeyboardMarkup


ADD_REMINDER_BUTTON = "➕ Añadir recordatorio"
VIEW_REMINDERS_BUTTON = "📋 Ver citas"
RESET_REMINDERS_BUTTON = "🗑️ Reset citas"
CANCEL_BUTTON = "❌ Cancelar"


MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [ADD_REMINDER_BUTTON],
        [VIEW_REMINDERS_BUTTON],
        [RESET_REMINDERS_BUTTON],
        [CANCEL_BUTTON]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)