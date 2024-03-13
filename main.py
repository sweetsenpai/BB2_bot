from telegram.ext import Application, CallbackQueryHandler, MessageHandler, \
    AIORateLimiter, filters, CommandHandler, ContextTypes, ConversationHandler, CommandHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import menu as menu
import logging
import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    application = Application.builder().token(token).rate_limiter(AIORateLimiter()).build()

    application.add_handler(CommandHandler('start', menu.start))

    application.add_handler(CallbackQueryHandler(pattern='C:', callback=menu.subcat_menu))

    application.run_polling()


if __name__ == '__main__':

    main()