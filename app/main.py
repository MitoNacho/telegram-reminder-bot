from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
)

from app.bot.conversations import (
    start_add_reminder,
    receive_title,
    receive_date,
    receive_time,
    confirm_reminder,
    cancel_conversation
)

from app.bot.handlers import (
    start_command,
    cancel_command,
    show_reminders,
    start_reset_reminders,
    confirm_reset_reminders,
    RESET_CONFIRMATION
)

from app.bot.states import (
    TITLE,
    DATE,
    TIME,
    CONFIRM
)

from app.config import BOT_TOKEN

from app.database.init_db import init_db

from app.scheduler.reminder_scheduler import start_scheduler


async def post_init(application):
    start_scheduler()

def main():
    init_db()

    application = (
    Application.builder()
    .token(BOT_TOKEN)
    .post_init(post_init)
    .build()
)
    

    add_reminder_conversation = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^➕ Añadir recordatorio$"),
                start_add_reminder
            )
        ],

        states={
            TITLE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    receive_title
                )
            ],

            DATE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    receive_date
                )
            ],

            TIME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    receive_time
                )
            ],

            CONFIRM: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    confirm_reminder
                )
            ]
        },

        fallbacks=[
            CommandHandler(
                "cancel",
                cancel_conversation
            )
        ]
    )

    reset_conversation = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^🗑️ Reset citas$"),
                start_reset_reminders
            )
        ],

        states={
            RESET_CONFIRMATION: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    confirm_reset_reminders
                )
            ]
        },

        fallbacks=[
    CommandHandler(
        "cancel",
        cancel_conversation
    ),

    MessageHandler(
        filters.Regex("^❌ Cancelar$"),
        cancel_conversation
    )
]
    )

    application.add_handler(
        CommandHandler("start", start_command)
    )

    application.add_handler(
        CommandHandler("cancel", cancel_command)
    )

    application.add_handler(
        MessageHandler(
            filters.Regex("^📋 Ver citas$"),
            show_reminders
        )
    )

    application.add_handler(add_reminder_conversation)

    application.add_handler(reset_conversation)

    print("Bot funcionando...")

    application.run_polling()


if __name__ == "__main__":
    
    main()