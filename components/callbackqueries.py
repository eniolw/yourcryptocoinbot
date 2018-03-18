# -*- coding: utf-8 -*-

"""
CryptoCoinBot is an open source project developed by @eniolw. 
<https://github.com/eniolw>
It is distributed under the GNU Affero General Public License 3.0
<https://fsf.org/>
"""

from telegram import (Bot, InlineKeyboardButton, InlineKeyboardMarkup,
                      InputTextMessageContent, InlineQueryResultArticle,
                      ParseMode)
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler,
                         InlineQueryHandler)
from telegram.ext.dispatcher import run_async

import templates
from cryptocoinmarket import CryptoCoinMarket


def callback_query_handler(self, bot, update):
    """Handlers callback queries triggered by inline buttons.

    Calls other functions to propperly handle the event produced by 
    inline buttons. So far two kinds of inline button are supported: 
    'top_list' and 'refresh'"""

    try:
      action = update.callback_query.data.split(";")[0]

    except IndexError:
        return
    
    actions = {
        "top": top_list_btn,
        "refresh": refresh_btn
    }
    func = actions.get(action, lambda: None)
    func(self, bot, update)


def top_list_btn(self, bot, update):
    """Updates the top list of cryptocurrencies previously sent."""

    query_id = update.callback_query.id
    chat_id, message_id, inline_message_id = get_target_data(update)
    
    try:
        top = int(update.callback_query.data.split(";")[1])

    except ValueError, IndexError:
        top = 10

    try:
        results = CryptoCoinMarket().ticker()

    except CryptoCoinMarket.ERROR:
        self.answerCallbackQuery(callback_query_id=query_id,
                                 text=text,
                                 show_alert=True)
        return

    text = templates.create_top_list(results, top=top)
    b1 = InlineKeyboardButton(text=templates.LabelButtons.TOP_10, 
                              callback_data="top;10")
    b2 = InlineKeyboardButton(text=templates.LabelButtons.TOP_30,
                              callback_data="top;30")
    b3 = InlineKeyboardButton(text=templates.LabelButtons.TOP_50,
                              callback_data="top;50")
    b4 = InlineKeyboardButton(text=templates.LabelButtons.TOP_100,
                              callback_data="top;100")
    grid = [[b1, b2], [b3, b4]]
    reply_markup = InlineKeyboardMarkup(grid)

    self.edit_message_text(chat_id=chat_id, 
                           message_id=message_id,
                           inline_message_id=inline_message_id,
                           text=text,
                           reply_markup=reply_markup,
                           parse_mode=ParseMode.HTML)

def refresh_btn(self, bot, update):
    """Updates the data about a cryptocurrency previoulsy sent."""

    query_id = update.callback_query.id
    chat_id, message_id, inline_message_id = get_target_data(update)
    coin = update.callback_query.data.split(";")[1]

    try:
        results = CryptoCoinMarket().ticker()

    except CryptoCoinMarket.ERROR:
        self.answerCallbackQuery(callback_query_id=query_id,
                                 text=templates.Texts.ERROR,
                                 show_alert=True)
        return

    found = None
    for result in results:
        if result.symbol == coin:
            found = result
            break

    if not found:
        text = templates.Texts.NO_LONGER_SUPPORTED
        self.edit_message_text(chat_id=chat_id, 
                               message_id=message_id, 
                               inline_message_id=inline_message_id,
                               text=text)
        return

    text = templates.create_summary(found)
    button = InlineKeyboardButton(text=templates.LabelButtons.REFRESH, 
                            callback_data="refresh;%s" % found.symbol)
    grid = [[button]]
    reply_markup = InlineKeyboardMarkup(grid)

    self.edit_message_text(chat_id=chat_id, 
                           message_id=message_id,
                           inline_message_id=inline_message_id,
                           text=text,
                           reply_markup=reply_markup,
                           parse_mode=ParseMode.HTML)
    
    self.answer_callback_query(callback_query_id=query_id,
                               text=templates.Texts.ALREADY_UPDATED,
                               show_alert=True)


def get_target_data(update):
    """Return three common values to send or update message:

    Args:

        'update': object created by the Telegram Bot API

    returns:
        A tuple containing: chat_id, message_id and 
        inline_message_od even if some of these are None

    """

    try:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
        inline_message_id = None

    except:
        chat_id = None
        message_id = None
        inline_message_id = update.callback_query.inline_message_id

    return chat_id, message_id, inline_message_id
