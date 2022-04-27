from itertools import groupby

from utils_classes import *


def one():
    f = open('data/1.txt', 'r')
    lines = f.readlines()
    sequences = []
    for line in lines:
        ints = [int(ele) for ele in line.split()]
        ints = filter(lambda x: x != -2, ints)
        split_at = -1
        raw_transactions = [list(g) for k, g in groupby(ints, lambda x: x != split_at) if k]

        transactions = []
        for raw_t in raw_transactions:
            items = list(map(lambda i: Item(i), raw_t))
            transaction = Transaction(items)
            transactions.append(transaction)
        sequences.append(Sequence(transactions))
    return sequences
