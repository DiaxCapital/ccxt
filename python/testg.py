import ccxt
import pprint

g = ccxt.gooplex()
# pprint.pprint(g.fetch_markets())
# g.load_markets()
# pprint.pprint(g.markets)
pprint.pprint(g.fetch_l2_order_book('TUSD/BTC'))
