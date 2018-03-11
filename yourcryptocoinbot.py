# -*- coding: utf-8 -*-
import coinmarketcap
from telegram.ext import Updater, CommandHandler


def start_function(bot, update):
    text = "Hi, welcome to Your CryptoCoin Bot! I will help you to search" \
           " the current price of many cryptocurrencies according to" \
           " coinmarketcap.com. Type /help for further information."
    update.message.reply_text(text)


def help_function(bot, update):
    text = "So far, I only support these commands:" \
            "\nstart: shows the introduction" \
            "\nhelp: shows this message" \
            "\nprice <cryptocoin_name>: searches the price of the specified cryptocurrency"
    update.message.reply_text(text)


def get_price(bot, update, args=None):

    # Checking if the user specified a cryptocurrency:
    if len(args) == 0:
        text = "You have to specify a cryptocoin. For example: /price bitcoin"
        update.message.reply_text(text)
        return

    # Joining all of the arguments to create an unique ID:
    currency_id = "-".join(args)

    # Requesting the price for the given cryptocurrency ID:
    marquet = coinmarketcap.Market()
    try:
        results = marquet.ticker(currency_id)
    except:
        text = "Something went wrong. Try later."
        update.message.reply_text(text)
        return
    
    # Checking if there are valid results:
    try:
        # Setting values for name and price (USD):
        coin_name = results[0]["name"]
        price_usd = results[0]["price_usd"]
    except:
        text = "Aparently, the cryptocurrency name you have given does not exist" \
               " or is not supported."
        update.message.reply_text(text)
    else:
        # Preparing and sending the answer:
        text = "%s price (USD): %s" % (coin_name, price_usd)
        update.message.reply_text(text)


def main():
    # Creating the Updater and dispatcher:
    updater = Updater("YOUR-TOKEN-HERE")
    dp = updater.dispatcher

    # Adding some CommandHandlers:
    dp.add_handler(CommandHandler("start", start_function))
    dp.add_handler(CommandHandler("help", help_function))

    # This CommandHandler will receive arguments from the user:
    dp.add_handler(CommandHandler("price", get_price, pass_args=True))

    # Running the bot through me polling method:
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()