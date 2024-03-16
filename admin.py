import os

import telegram.error
from dotenv import load_dotenv
from telegram.ext import Application, CallbackQueryHandler, MessageHandler, \
    AIORateLimiter, filters, CommandHandler, ContextTypes, ConversationHandler, CommandHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import logging
from db import Categories, Subcategories, Sub_Masters, Masters, Images, session
import os
from dotenv import load_dotenv

load_dotenv()


async def store_img(context: ContextTypes.DEFAULT_TYPE):
    images_preload = session.query(Images).where(Images.telegram_file_id == None).all()
    for image in images_preload:
        image.telegram_file_id = (await context.bot.send_photo(chat_id=os.environ.get("MYID"), photo=image.img_url)).photo[0].file_id
        session.commit()
    return


async def master_moderation(context: ContextTypes.DEFAULT_TYPE):
    masters_for_mod = session.query(Masters).where(Masters.need_moderation == True).all()
    for master in masters_for_mod:
        await context.bot.send_message(chat_id=os.environ.get("MYID"), text='Мастер обновил свой профиль!')
        await context.bot.send_message(chat_id=os.environ.get("MYID"), text=master.tg_msg(), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Сделать видимым', callback_data=f'V:{master.master_id}')]]))
    return


async def make_master_visable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    master_id = int(update.callback_query.data.replace('V:', ''))
    master = session.query(Masters).where(Masters.master_id == master_id).one()
    master.visability = True
    master.need_moderation = False
    session.commit()
    await update.callback_query.edit_message_text(text=f'Мастер {master.name} теперь виден пользователям.')
    return