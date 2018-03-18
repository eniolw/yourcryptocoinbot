# -*- coding: utf-8 -*-

"""
CryptoCoinBot is an open source project developed by @eniolw. 
<https://github.com/eniolw>
It is distributed under the GNU Affero General Public License 3.0
<https://fsf.org/>
"""

import random


class Texts(object):

	START = "Hi, welcome to Your CryptoCoin Bot! I will help you to search" \
	        " information on cryptocurrency market capitalizations according to" \
	        " coinmarketcap.com. Type /help for further information."

	HELP = "So far, I support these commands:" \
	       "\n<code>/start</code>: shows the introduction" \
	       "\n<code>/help</code>: shows this message" \
	       "\n<code>/search &lt;cryptocoin_name&gt;</code>:" \
           " searches the price of the specified cryptocurrency. if no name is given" \
           " then menus to select a cryptocurrency will be displayed." \
           "\n<code>/list</code>: shows a top list of Cryptocurrency Market Capitalizations" \
           "\nYou can use me in <b>inline mode</b>. Just type @yourcryptocoinbot and the" \
           " name of any cryptocurrency. For example: <code>@yourcryptocoinbot BTC</code>"

	ERROR = "❌ Something went wrong. Try later."

	PRESS_BUTTON = "☝️ Tap one button to display some results:" \

	NO_SUPPORTED = "🤔 Aparently, that name doesn't correspond to a supported cryptocurrency"

	NO_LONGER_SUPPORTED = "🤷‍♂️ [UPDATE] Sorry. Aparently, this cryptocurrency is no longer supported."

	ALREADY_UPDATED = "✅ Already updated!"


class LabelButtons(object):

	REFRESH = "🔁 Refresh"

	PAG = "Pag"

	TOP_10, TOP_30, TOP_50, TOP_100 = "Top 10", "Top 30", "Top 50", "Top 100"

                  
def create_top_list(results, **kwargs):
    """Returns a top list of crypto currency capitalizations."""

    html = "ℹ️ <b>Crypto Currency Capitalizations</b>"
    html += "\nTOP %s:" % kwargs.get("top", len(results))
    for i, result in enumerate(results):
        html += "\n" if i % 10 == 0 else ""
        html += "\n%s. %s: $<b>%s</b>" % (i + 1, result.name, result.price_usd)
        if i + 1 >= kwargs.get("top", len(results)):
        	break

    return html


def create_summary(result, **kwargs):
    """Returns a text with detailed info about a specific cryptocurrency. """

    emojie = random.choice(("🔸", "🔹", "▪️", "▫️", "🔘"))
    html = "%s <b>%s (%s)</b>" % (emojie, result.name, result.symbol)
    html += "\n<i>Price (USD): {:,}</i>".format(result.price_usd)
    html += "\nPrice (BTC): {:,}".format(result.price_btc)
    html += "\nRank: {0}".format(result.rank)
    html += "\nVolume (24h): {:,}".format(result.volume_usd_24h)
    html += "\nCirculating supply: {:,}".format(result.available_supply)
    html += "\nChange (24h): {:,}".format(result.percent_change_24h)

    return html