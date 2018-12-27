# AV_data_acc
Accumulate Alpha vantage data 5min for selected tickers

```
usage: acc1.py [-h] [--ticker-csv TICKER_CSV] [--interval INTERVAL]
               [--readsize READSIZE] [--filepath FILEPATH]
               [--fileprefix FILEPREFIX]

optional arguments:
  -h, --help            show this help message and exit
  --ticker-csv TICKER_CSV
                        The file store ticker names. It is required to be a
                        CSV and sep by comma.
  --interval INTERVAL   The AV default time intervals intra day, default is
                        5min. it can be 60min, 1min.
  --readsize READSIZE   compact or full. Default is compact.
  --filepath FILEPATH   The stock data store dir.
  --fileprefix FILEPREFIX
                        The filename prefix before the the ticker name.
```
