# import pandas as pd
import pickle
import bz2


def read_data(filename):
    with bz2.BZ2File(filename) as pfile_handle:
        old_data = pickle.load(pfile_handle)
    return old_data


class yaoshi:
    def __init__(self):
        self.df = read_data("inputs.p.bz2")
        self.avkeys = self.df[self.df['lock'] == 'av']['key'].values.T.tolist()
        self.fredkeys = self.df[self.df['lock']
                                == 'fred']['key'].values.T.tolist()


def main():
    key = yaoshi()
    print("av ", key.avkeys)
    print("fred ", key.fredkeys)


if __name__ == "__main__":
    main()
