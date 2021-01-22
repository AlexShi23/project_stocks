import os, tinvest, datetime, json, schedule
from datetime import datetime, timedelta
from tinvest import SyncClient

TOKEN = os.getenv('TINVEST_SANDBOX_TOKEN', 't.0Lfr5gsb96J5MyCi2sbPj1gzS55r2PCvJ5bYLNkSlPcnEMfMIrfr21zyqq8DvU-W5r-7jcbqDrPGUrWBqjFcVw')
client = SyncClient(TOKEN, use_sandbox=True)

def get_data(figi):
    dt_now = datetime.now()
    dt_last = datetime.now() - timedelta(minutes=30)
    note = { }
    candles = client.get_market_candles(figi, dt_last.strftime("%Y-%m-%dT%H:%M:%S.000000+03:00"), dt_now.strftime("%Y-%m-%dT%H:%M:%S.000000+03:00"), tinvest.CandleResolution('1min')).payload.candles
    if (len(candles) > 0):
        note.update(candles[len(candles)-1])
    # note.update(client.get_market_orderbook(figi, 20).payload) добавляем стакан
    return note
    
def write_to_file(filename, note):
    with open('data/' + filename + '.json', 'a+') as f:
        json.dump(note, f, default=str)

def parse(securities):
    for figi, name in securities.items():
        write_to_file(name, get_data(figi))

def init():
    bonds = client.get_market_bonds()
    etfs = client.get_market_etfs()
    stocks = client.get_market_stocks()

    securities = { }
    for bond in bonds.payload.instruments:
        securities[bond.figi] = bond.name
    for etf in etfs.payload.instruments:
        securities[etf.figi] = etf.name
    for stock in stocks.payload.instruments:
        securities[stock.figi] = stock.name
    return securities

def main():
    sec = init()
    schedule.every(1).minutes.do(parse(sec))

    while 1:
        schedule.run_pending()
        datetime.sleep(1)


if (__name__ == '__main__'):
    main()

# note = { }
# note.update(client.get_market_candles('BBG0013HGFT4', '2020-12-25T10:10:00.000000+03:00', '2020-12-25T10:11:00.000000+03:00', tinvest.CandleResolution('1min')).payload.candles[0])
# note.update(client.get_market_orderbook('BBG0013HGFT4', 20).payload)
# print(note)
# write_to_file('1', note)