from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import argparse
import pickle
import bz2
import numpy as np
import time
import os
import logging
import yaoshi

TIME_OUT = 3  # time out sec = TIME_OUT * TIME_WAIT sec
TIME_WAIT = 120
TICKER_FILE = "ticker.csv"
# ticker_list = pd.read_csv(TICKER_FILE, sep=',')


def print_log(message):
    logging.info(message)
    print(message)


def read_stock_AV(keys, symbol='QQQ', interval='5min', outputsize='compact'):
    ts = TimeSeries(key=keys[np.random.randint(len(keys))],
                    output_format='pandas', indexing_type='date')
    result = None
    timeout = 0
    while result is None:
        try:
            # connect AV
            result, _ = ts.get_intraday(
                symbol=symbol, interval=interval, outputsize=outputsize)
        except:
            if timeout < TIME_OUT:
                time.sleep(TIME_WAIT)
                timeout = timeout + 1
                pass
            else:
                print_log("Time out %s" % symbol)
                return None
    print_log("read %s from av [ %s to %s ]" % (symbol,
                                                result.index[0],
                                                result.index[-1]
                                                ))
    return result


def read_data(symbol, filepath="data/", fileprefix=""):
    filename = filepath + fileprefix + symbol + ".p.bz2"
    with bz2.BZ2File(filename) as pfile_handle:
        old_data = pickle.load(pfile_handle)
    return old_data


def write_data(symbol, df, filepath="data/", fileprefix=""):
    filename = filepath + fileprefix + symbol + ".p.bz2"
    if os.path.isfile(filename):
        old_data = read_data(symbol, filepath, fileprefix)
        df = pd.concat([df, old_data])  # .drop_duplicates().sort_index()
        df = df[~df.index.duplicated(keep='first')]
        df = df.sort_index()
    with bz2.BZ2File(filename, "w") as pfile:
        pickle.dump(df, pfile,
                    protocol=pickle.HIGHEST_PROTOCOL)


def dispatch(ticker_csv,
             interval,
             readsize,
             filepath,
             fileprefix
             ):
    print(os.listdir("."))
    timestr = time.strftime("%Y%m%d-%H%M%S")
    logging.basicConfig(filename='log/' + timestr + '.log',
                        format='%(asctime)s %(message)s',
                        level=logging.INFO)

    ticker_list = pd.read_csv(ticker_csv, sep=',')
    key = yaoshi.yaoshi()

    for ticker in ticker_list['Ticker']:
        df = read_stock_AV(keys=key.avkeys, symbol=ticker, interval=interval,
                           outputsize=readsize)
        if df is not None:
            print("=============================",
                  "\n", "read and write", ticker)
            print(df.head(1).append(df.tail(1)))
            write_data(ticker, df, filepath=filepath, fileprefix=fileprefix)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker-csv',
                        default=TICKER_FILE,
                        type=str,
                        help='The file store ticker names. It is required to be a CSV and sep by comma.')
    parser.add_argument('--interval',
                        default="5min",
                        type=str,
                        help='The AV default time intervals intra day, default is 5min. it can be 60min, 1min.')
    parser.add_argument('--readsize',
                        default="compact",
                        type=str,
                        help='compact or full. Default is compact.')
    parser.add_argument('--filepath',
                        type=str,
                        default="data/",
                        help="The stock data store dir.")
    parser.add_argument('--fileprefix',
                        type=str,
                        default='',
                        help="The filename prefix before the the ticker name.")
    parse_args, unknown = parser.parse_known_args()

    dispatch(**parse_args.__dict__)
