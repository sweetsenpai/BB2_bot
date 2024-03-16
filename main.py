from telegram.ext import Application, CallbackQueryHandler, MessageHandler, \
    AIORateLimiter, filters, CommandHandler, ContextTypes, ConversationHandler, CommandHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import menu as menu
import admin as admin
import logging
import os
from dotenv import load_dotenv

load_dotenv()
# TODO: DOCKER
token = os.environ.get("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    application = Application.builder().token(token).rate_limiter(AIORateLimiter()).build()

    application.add_handler(CommandHandler('start', menu.start))

    application.add_handler(CallbackQueryHandler(pattern='BC', callback=menu.start))
    application.add_handler(CallbackQueryHandler(pattern='C:', callback=menu.subcat_menu))
    application.add_handler(CallbackQueryHandler(pattern='S:', callback=menu.master_menu))
    application.add_handler(CallbackQueryHandler(pattern='M:', callback=menu.show_master_data))
    application.add_handler(CallbackQueryHandler(pattern='V:', callback=admin.make_master_visable))
    application.add_handler(CallbackQueryHandler(pattern='P:', callback=menu.show_master_images))

    application.job_queue.run_repeating(callback=admin.store_img, first=0, interval=180)
    application.job_queue.run_repeating(callback=admin.master_moderation, first=0, interval=180)

    application.run_polling()


if __name__ == '__main__':

    main()