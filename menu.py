from telegram.ext import Application, CallbackQueryHandler, MessageHandler, \
    AIORateLimiter, filters, CommandHandler, ContextTypes, ConversationHandler, CommandHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import logging
from db import Categories, Subcategories, Masters, Images, session


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories = session.query(Categories).all()
    cat_menu = []
    for cat in categories:
        cat_menu.append([InlineKeyboardButton(text=cat.cat_name, callback_data=f'C:{cat.cat_id}')])
    await update.message.reply_text('Выбери категорию:', reply_markup=InlineKeyboardMarkup(cat_menu))
    return


async def subcat_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cat_id = int(update.callback_query.data.replace('C:', ''))
    print(cat_id)
    subcatigories = session.query(Subcategories).where(Subcategories.sub_cat_id==cat_id).all()
    sub_menu = []
    for sub in subcatigories:

        sub_menu.append([InlineKeyboardButton(text=sub.sub_name, callback_data=f'S{sub.sub_id}')])
    sub_menu.append([InlineKeyboardButton(text='Назад', callback_data=f'Back')])
    await update.callback_query.edit_message_text('Выбери подкатегорию:', reply_markup=InlineKeyboardMarkup(sub_menu))
    return