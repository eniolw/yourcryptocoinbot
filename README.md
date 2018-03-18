# About
**Your Crypto Coin Bot** [@Yourcryptocoinbot](https://telegram.me/yourcryptocoinbot)is a Telegram bot to search cryptocurrency market capitalizations according to [coinmarketcap.com](https://coinmarketcap.com). This is a project started by @eniolw (eniolw@gmail.com; Telegram: [BotFather](https://telegram.me/eniolw); Steemit: [@eniolw](https://steemit.com/@eniolw/). You can visit this blog to know more about the development of this project and others.


# Deploy it
YourCryptoCoinBot is already running and working on Telegram (@yourcryptocoinbot). However, you can clone or fork this project and deploy it yourself.

* Create a Bot account on Telegram and get a token. Talk to [BotFather](https://telegram.me/botfather) for this.
* Then, run this:

```
sudo pip install python-telegram-bot
sudo pip install coinmarketcap
```

* Clone this [repository on Github](https://github.com/eniolw/yourcryptocoinbot)
* Replace the `YOUR_TOKEN` string in the `main` function (file: `yourcryptocoinbot.py`) with your own token previously given by Botfather.
* Run the `yourcryptocoinbot.py` script like this: `python yourcryptocoinbot.py`.


# Acknowledgements
This bot was built with the help of these open source libraries: [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) and [coinmarketcap](https://github.com/barnumbirr/coinmarketcap). The latter is in turn a wrapper to the [Crypto Market Capitalizations API](https://coinmarketcap.com/api/).

Thanks to Riztan Gutiérrez (Telegram:  @riztan) por hosting the bot.
