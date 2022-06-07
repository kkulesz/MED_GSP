from matplotlib import pyplot as plt
import pandas as pd


def my_plot(df, title):
    plt.plot(df['Number of sequences'], df['Execution time'])
    plt.xlabel('Number of sequences')
    plt.ylabel('Execution time[s]')
    plt.title(title)
    plt.show()


if __name__ == '__main__':
    f1 = '../results-BMS1_spmf.txt.csv'
    f2 = '../results-MT745584_SPMF.txt.csv'

    d1 = pd.read_csv(f1)
    d2 = pd.read_csv(f2)

    my_plot(d1, 'BMS1_spmf')
    my_plot(d2, 'MT745584_SPMF')

