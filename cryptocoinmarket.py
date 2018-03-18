# -*- coding: utf-8 -*-

"""
CryptoCoinBot is an open source project developed by @eniolw. 
<https://github.com/eniolw>
It is distributed under the GNU Affero General Public License 3.0
<https://fsf.org/>
"""

import coinmarketcap


class CrytoCoinData(object):

    """
    A model for the incoming data from cryptocoin.com API
    """

    def __init__(self,
                 id, 
                 name, 
                 symbol, 
                 price_usd, 
                 price_btc, 
                 rank,
                 volume_usd_24h,
                 percent_change_24h,
                 available_supply,
                 **kwargs):

        self.id = id.encode("utf-8")
        self.name = name.encode("utf-8")
        self.symbol = symbol.encode("utf-8")
        self.price_usd = float(price_usd)
        self.price_btc = float(price_btc)
        self.rank = int(rank)
        self.volume_usd_24h = float(volume_usd_24h)
        self.percent_change_24h = float(percent_change_24h)
        self.available_supply = float(available_supply)

    def __str__(self):
        return "%s %s %s %s %s %s %s %s %s" % (self.id, self.name, self.symbol, 
                                               self.price_usd, self.price_btc, 
                                               self.rank, self.volume_usd_24h, 
                                               self.percent_change_24h, 
                                               self.available_supply)


class CryptoCoinMarketError(Exception):
    pass


class CryptoCoinMarket(object):

    """
    Wrapper to retrieve data using the coinmarketcap module but 
    converting it into a appropiate model
    """

    ERROR = CryptoCoinMarketError

    def ticker(currency=None):
        """
        Retrieves data from coinmarketcap.com API using the
        coinmarketcap module and converts it into a CryptoCoinData
        instance. Returns an arrange of CryptoCoinData
        """

        try:
            results = coinmarketcap.Market().ticker()

        except:
            raise self.ERROR
            return

        data = [CrytoCoinData(res.get("id"),
                              res.get("name"),
                              res.get("symbol"),
                              res.get("price_usd"),
                              res.get("price_btc"),
                              res.get("rank"),
                              res.get("24h_volume_usd"),
                              res.get("percent_change_24h"),
                              res.get("available_supply"))
                for res in results]

        return data


# Instance to be imported:
market = CryptoCoinMarket()