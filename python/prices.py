import datetime
import pprint

from ccxt.gooplex import gooplex

since = datetime.datetime(2021, 5, 27, 0, 0, 0)
since = int(since.timestamp() * 1000)
result = {}

g = gooplex()
market = g.load_markets()
for symbol in market.keys():
    (buy, sell) = symbol.split('/')
    sell = sell.lower()
    if sell not in ('usdt', 'btc'):
        print('(Ignoring {})'.format(symbol))
        continue

    if buy not in result:
        result[buy] = {}

    print('OHLCV of', symbol)
    ohlcv = g.fetch_ohlcv(symbol,
                          since=since,
                          limit=100_000,
                          timeframe='1d')
    for entry in ohlcv:
        (timestamp, _open, high, low, close, volume) = entry
        date = datetime.datetime\
            .fromtimestamp(timestamp / 1000)\
            .strftime('%Y-%m-%d')
        if date not in result[buy]:
            result[buy][date] = {}

        print('\t{date}/{sell} = {close}'.format(
            date=date,
            sell=sell,
            close=close))
        result[buy][date][sell] = close

with open('fechamento.tsv', 'w') as target:
    for (symbol, symbol_dates) in result.items():
        for (date, values) in symbol_dates.items():
            target.write('{symbol}\t'
                         '{date}\t'
                         '{usdt:.8f}\t'
                         '{btc:.8f}\n'.format(
                             symbol=symbol,
                             date=date,
                             usdt=(values['usdt']
                                   if 'usdt' in values
                                   else 0),
                             btc=(values['btc']
                                  if 'btc' in values
                                  else 0)))
