from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import argparse
import pickle
import bz2
import numpy as np
import time
import os

TICKER_FILE = "ticker.csv"
# ticker_list = pd.read_csv(TICKER_FILE, sep=',')


def read_stock_AV(symbol='QQQ', interval='5min', outputsize='compact'):
    keys = ['EYDTQCC46AZBZH20', 'Q0GC0ZMPBB7GFHTL',
            'EJ69MPM068NGTJ30', 'XTLCDXQK9034JC9S',
            '8KZI0IZQ3UVXJ589', 'KDXMV58WTWWABHKB']
    ts = TimeSeries(key=keys[np.random.randint(len(keys))],
                    output_format='pandas', indexing_type='date')
    result = None
    while result is None:
        try:
            # connect AV
            result, _ = ts.get_intraday(
                symbol=symbol, interval=interval, outputsize=outputsize)
        except:
            time.sleep(20)
            pass
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
    ticker_list = pd.read_csv(ticker_csv, sep=',')

    for ticker in ticker_list['Ticker']:
        df = read_stock_AV(symbol=ticker, interval=interval,
                           outputsize=readsize)
        print("=============================", "\n", "read and write", ticker)
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
