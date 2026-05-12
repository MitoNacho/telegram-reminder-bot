from telegram import ReplyKeyboardMarkup


MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        ["➕ Añadir recordatorio"],
        ["📋 Ver citas"],
        ["🗑️ Reset citas"],
        ["❌ Cancelar"]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)