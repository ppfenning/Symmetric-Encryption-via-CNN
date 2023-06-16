import pandas as pd

id_map = pd.read_csv('../data/speaker-info.txt').set_index('ID', drop=True).to_dict(orient='index')

if __name__ == '__main__':
    print(id_map)