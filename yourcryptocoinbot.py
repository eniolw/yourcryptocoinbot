#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CryptoCoinBot is an open source project developed by @eniolw. 
<https://github.com/eniolw>
It is distributed under the GNU Affero General Public License 3.0
<https://fsf.org/>
"""

import logging
from telegram import (Bot, InlineKeyboardButton, InlineKeyboardMarkup,
                      InputTextMessageContent, InlineQueryResultArticle,
                      ParseMode)
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler,
                         InlineQueryHandler)
from telegram.ext.dispatcher import run_async

import components
import templates
from cryptocoinmarket import CryptoCoinMarket


class CryptoCoinBot(object):

    def __init__(self, token):

        # Creating the Updater and the dispatcher:
        self.logger = logging.getLogger(__name__)
        self.bot = Bot(token)
        self.updater = Updater(token)
        dp = self.updater.dispatcher

        # Adding some CommandHandlers:
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("help", self.help))

        # This CommandHandler will receive arguments from the user:
        dp.add_handler(CommandHandler("search", self.search, pass_args=True))
        dp.add_handler(CommandHandler("list", self.get_list))

        # These will handler callback queries and inline queries:
        dp.add_handler(CallbackQueryHandler(self.callback_query_handler)) 
        dp.add_handler(InlineQueryHandler(self.inline_query_handler))

        # Log all errors:
        dp.add_error_handler(self.error)


    def start_polling(self):
        """starts the polling to run the bot."""

        self.updater.start_polling()
        self.updater.idle()

    def error(self, bot, update, err):
        """Logs all errors."""

        self.logger.warning("update {0} caused error {1}" % (update, err))

    def start(self, bot, update):
        """Handlers the 'start' command."""

        chat_id = update.message.chat_id
        self.send_message(chat_id, templates.Texts.START, parse_mode=ParseMode.HTML)

    def help(self, bot, update):
        """Handlers the 'help' command."""

        chat_id = update.message.chat_id
        self.send_message(chat_id, templates.Texts.HELP, parse_mode=ParseMode.HTML)

    def search(self, bot, update, args=None):
        """Handlers the 'price' command.""

        This command is meant to get the data about the cryptocurrency that
        the user specifies with arguments. If the user doesn't specify a
        cryptocurrency, the function will sent a menu of buttons in order to
        choose a cryptocurrency"""

        chat_id = update.message.chat_id

        # Requesting the price for the given cryptocurrency ID:
        try:
            results = CryptoCoinMarket().ticker()

        except CryptoCoinMarket.ERROR:
            self.send_message(chat_id, templates.Texts.ERROR)
            return

        # Checking if the user specified a cryptocurrency:
        if not args:
            l = len(results)
            n = l / 50 if l % 50 == 0 else l / 50 + 1
            rows = [InlineKeyboardButton(text="%s %s" % (templates.LabelButtons.PAG, i + 1), 
                                         switch_inline_query_current_chat="+p %s" % (i + 1))
                                         for i in range(n)]
            grid = [rows]
            reply_markup = InlineKeyboardMarkup(grid)
            self.send_message(chat_id, 
                              templates.Texts.PRESS_BUTTON, 
                              reply_markup=reply_markup, 
                              parse_mode=ParseMode.HTML)
            return

        # Joining all of the arguments to create an unique ID:
        data = "-".join(args).lower()
    
        # Searching:
        found = None
        for result in results:
            if data == result.id or data == result.symbol.lower():
                found = result
                break

        if not found:
            self.send_message(chat_id, templates.Texts.NO_SUPPORTED)
            return

        # Preparing and sending the answer:
        text = templates.create_summary(found)
        button = InlineKeyboardButton(text=templates.LabelButtons.REFRESH,
                                      callback_data="refresh;%s" % found.symbol)
        grid = [[button]]
        reply_markup = InlineKeyboardMarkup(grid)

        self.send_message(chat_id, text, reply_markup=reply_markup, 
                          parse_mode=ParseMode.HTML)

    def get_list(self, bot, update):
        """Handlers for the 'list' command.

        This command is meant to send a top list about the capitalization
        of cryptocurrencies. By default, the top value is set to 10, but the
        user is also allowed to choose among top 30, top 50 and top 100"""

        chat_id = update.message.chat_id
        try:
            results = CryptoCoinMarket().ticker()

        except CryptoCoinMarket.ERROR:
            self.send_message(chat_id, templates.Texts.ERROR)
            return

        text = templates.create_top_list(results, top=10)
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

        self.send_message(chat_id, text, reply_markup=reply_markup, 
        parse_mode=ParseMode.HTML)


    def callback_query_handler(self, bot, update):
        """Handlers the callback_queries through an imported function."""
        
        components.callback_query_handler(self, bot, update)

    def inline_query_handler(self, bot, update):
        """Handlers the inline_queries through an imported function."""
        
        components.inline_query_handler(self, bot, update)

    @run_async
    def send_message(self, *args, **kwargs):
        """Runs this TelegramBot method in a separated thread."""

        self.bot.sendMessage(*args, **kwargs)

    @run_async
    def edit_message_text(self, *args, **kwargs):
        """Runs this TelegramBot method in a separated thread."""

        self.bot.editMessageText(*args, **kwargs) 

    @run_async
    def answer_inline_query(self, *args, **kwargs):
        """Runs this TelegramBot method in a separated thread."""

        self.bot.answerInlineQuery(*args, **kwargs)

    @run_async
    def answer_callback_query(self, *args, **kwargs):
        """Runs this TelegramBot method in a separated thread."""

        self.bot.answerCallbackQuery(*args, **kwargs)


def main():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    token = "534987830:AAE7U_W83yK32vICGmo4ep9fW7uAsRpDe8A"
    crypto_coin_tbot = CryptoCoinBot(token) 
    crypto_coin_tbot.start_polling()


if __name__ == '__main__':
    main()