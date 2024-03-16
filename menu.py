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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories = session.query(Categories).all()
    cat_menu = []
    for cat in categories:
        cat_menu.append([InlineKeyboardButton(text=cat.cat_name, callback_data=f'C:{cat.cat_id}')])
    try:
        await update.message.reply_text('Выбери категорию:', reply_markup=InlineKeyboardMarkup(cat_menu))
    except AttributeError:
        await update.callback_query.edit_message_text(text='Выбери категорию:', reply_markup=InlineKeyboardMarkup(cat_menu))
    return


async def subcat_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cat_id = int(update.callback_query.data.replace('C:', ''))
    subcatigories = session.query(Subcategories).where(Subcategories.sub_cat_id == cat_id).all()
    if subcatigories is None:
        await update.callback_query.answer(text='Пока тут пусто(')
    sub_menu = []
    for sub in subcatigories:

        sub_menu.append([InlineKeyboardButton(text=sub.sub_name, callback_data=f'S:{sub.sub_id}')])
    sub_menu.append([InlineKeyboardButton(text='Назад', callback_data=f'BC')])
    await update.callback_query.edit_message_text('Выбери подкатегорию:', reply_markup=InlineKeyboardMarkup(sub_menu))
    return


async def master_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sub_id = int(update.callback_query.data.replace('S:', ''))
    cat_id = session.query(Subcategories).where(Subcategories.sub_id == sub_id).one().sub_cat_id
    sub_masters = session.query(Sub_Masters).where(Sub_Masters.subcategories_id == sub_id).all()
    m_menu = []
    for s_m in sub_masters:
        master_data = session.query(Masters).where(Masters.master_id == s_m.masters_id).one()
        m_menu.append([InlineKeyboardButton(text=master_data.name, callback_data=f'M:{master_data.master_id}:{sub_id}')])
    m_menu.append([InlineKeyboardButton(text='Назад', callback_data=f'C:{cat_id}')])
    await update.callback_query.edit_message_text('Выбери местера:', reply_markup=InlineKeyboardMarkup(m_menu))
    return


async def show_master_data(update: Update, context: ContextTypes.DEFAULT_TYPE):

    master_id, sub_id = update.callback_query.data.replace('M:', '').split(':')
    master = session.query(Masters).where(Masters.master_id == int(master_id)).one()
    master_buttons = [[InlineKeyboardButton(text='Примера работ', callback_data=f'P:{master_id}:0:{sub_id}')], [InlineKeyboardButton(text='Назад', callback_data=f'S:{sub_id}')]]
    try:
        await update.callback_query.edit_message_text(text=master.tg_msg(), reply_markup=InlineKeyboardMarkup(master_buttons))
    except telegram.error.BadRequest:
        callback_data = update.callback_query
        await context.bot.delete_message(chat_id=callback_data.from_user.id, message_id=callback_data.message.message_id)
        await context.bot.send_message(chat_id=callback_data.from_user.id, text=master.tg_msg(), reply_markup=InlineKeyboardMarkup(master_buttons))
    return


async def show_master_images(update: Update, context: ContextTypes.DEFAULT_TYPE):

    ids = (update.callback_query.data.replace('P:', ''))
    master_id, page, sub_id = ids.split(':')
    master_images = session.query(Images).where(Images.master_img_id == int(master_id)).all()
    page = int(page)

    callback_data = update.callback_query
    await context.bot.delete_message(chat_id=callback_data.from_user.id, message_id=callback_data.message.message_id)
    imag_inline = []
    if page - 1 >= 0:
        imag_inline.append([InlineKeyboardButton(text='⬅️', callback_data=f'P:{master_id}:{page - 1}:{sub_id}')])
    if page + 1 <= len(master_images) - 1:
        if imag_inline:
            imag_inline[0].append(InlineKeyboardButton(text='➡️', callback_data=f'P:{master_id}:{page+1}:{sub_id}'))
        else:
            imag_inline.append([InlineKeyboardButton(text='➡️', callback_data=f'P:{master_id}:{page+1}:{sub_id}')])
    imag_inline.append([InlineKeyboardButton(text='Назад', callback_data=f'M:{master_id}:{sub_id}')])

    await context.bot.send_photo(chat_id=callback_data.from_user.id,
                                 photo=master_images[page].telegram_file_id,
                                 caption=master_images[page].description, reply_markup=InlineKeyboardMarkup(imag_inline))

    return




