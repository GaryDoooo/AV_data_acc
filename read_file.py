import pandas
import pickle
import bz2


def read_data(symbol, filepath="data/", fileprefix=""):
    filename = filepath + fileprefix + symbol + ".p.bz2"
    with bz2.BZ2File(filename) as pfile_handle:
        old_data = pickle.load(pfile_handle)
    return old_data



if __name__ == "__main__":
    print(read_data('AAPL')) 
