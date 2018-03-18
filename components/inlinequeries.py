# -*- coding: utf-8 -*-

"""
CryptoCoinBot is an open source project developed by @eniolw. 
<https://github.com/eniolw>
It is distributed under the GNU Affero General Public License 3.0
<https://fsf.org/>
"""

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      InputTextMessageContent, InlineQueryResultArticle,
                      ParseMode)
from telegram.ext.dispatcher import run_async
from uuid import uuid4

import templates
from cryptocoinmarket import CryptoCoinMarket


def inline_query_handler(self, bot, update):
    """Handlers inline queries.

    Calls other functions to propperly handle the event produced by 
    inline queries. So far, two kinds of inline queries are supported: 
    1) '+p \d+' for example: '+p 1', '+p 2' and 2) '{cryptocurrency name}'
    both handled by the default_action function"""

    try:
        action = update.inline_query.query.split()[0]

    except IndexError:
        action = ""

    actions = {}
    func = actions.get(action, default_action)
    func(self, bot, update)


def default_action(self, bot, update):
    """Calls the default_method to handle the incoming data."""

    query = update.inline_query.query
    if query == "":
        pass

    elif not query.startswith("+"):
        search_cryptocurrency_info(self, bot, update)

    elif query.startswith("+p "):
        display_general_list(self, bot, update)
        
    else:
        pass


def search_cryptocurrency_info(self, bot, update):
    """Sends articles according to the input data."""

    try:
        results = CryptoCoinMarket().ticker()

    except CryptoCoinMarket.ERROR:
        return

    # Searching:
    data = update.inline_query.query.strip()
    found = []
    for result in results:
        if result.name.lower().startswith(data.lower()) \
        or result.symbol.startswith(data.upper()):
            found.append(result)

    if len(found) == 0:
        return    

    articles = []
    for result in found:
        title = "(%s) %s" % (result.rank, result.symbol)
        description = "%s (%s)" % (result.name, result.price_usd)
        txt = templates.create_summary(result)
        txt = InputTextMessageContent(txt, parse_mode=ParseMode.HTML)
        blabel = templates.LabelButtons.REFRESH
        bdata = "refresh;%s" % result.symbol
        button = InlineKeyboardButton(text=blabel, 
                                      callback_data=bdata)
        grid = [[button]]
        reply_markup = InlineKeyboardMarkup(grid)
        art = InlineQueryResultArticle(id=uuid4(),
                                       title=title,
                                       input_message_content=txt,
                                       reply_markup=reply_markup,
                                       description=description)
        articles.append(art)

        if len(articles) == 50:
            break

    self.answer_inline_query(update.inline_query.id, articles)


def display_general_list(self, bot, update):
    """Sends up to 50 articles each with a specific cryptocurrency info."""

    def set_number(data):
        try:
            return int(data)

        except ValueError:
            return 1

    query = update.inline_query.query.split()
    pag = 1 if len(query) == 1 else set_number(query[1])
    
    try:
        results = CryptoCoinMarket().ticker()

    except CryptoCoinMarket.ERROR:
        return

    l = len(results)
    n = l / 50 if l % 50 == 0 else l / 50 + 1                
    x1 = pag * 50 - 50 if 0 < pag <= n else 0
    x2 = pag * 50 if 0 < pag <= n else 50
    results = results[x1:x2]
    articles = []

    for i, result in enumerate(results):
        title = "%s. %s" % (result.rank, result.symbol)
        description = "%s (%s)" % (result.name, result.price_usd)
        txt = templates.create_summary(result)
        txt = InputTextMessageContent(txt, parse_mode=ParseMode.HTML)
        blabel = templates.LabelButtons.REFRESH
        bdata = "refresh;%s" % result.symbol
        button = InlineKeyboardButton(text=blabel, 
                                      callback_data=bdata)
        grid = [[button]]
        reply_markup = InlineKeyboardMarkup(grid)
        art = InlineQueryResultArticle(id=uuid4(),
                                       title=title,
                                       input_message_content=txt,
                                       reply_markup=reply_markup,
                                       description=description)
        articles.append(art)


    self.answer_inline_query(update.inline_query.id, articles)