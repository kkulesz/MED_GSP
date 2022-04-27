from typing import List
from itertools import groupby

from without_time.utils_classes import *


def read_and_convert(filepath):
    f = open(filepath, 'r')
    file_str = f.read()
    ints = [int(ele) for ele in file_str.split()]

    split_at = -2  # '-2' is delimiter between sequences
    raw_sequences_ints = [list(g) for k, g in groupby(ints, lambda x: x != split_at) if k]
    sequences = []
    for sequence_ints in raw_sequences_ints:
        split_at = -1  # '-1' is delimiter between transactions
        raw_transactions_ints = [list(g) for k, g in groupby(sequence_ints, lambda x: x != split_at) if k]
        transactions = []
        for raw_t in raw_transactions_ints:
            items = list(map(lambda i: Item(i), raw_t))
            transactions.append(Transaction(items))
        sequences.append(Sequence(transactions))

    return sequences


def convert_list(raw_sequences):
    result_sequences: List[Sequence] = []
    for raw_sequence in raw_sequences:
        transactions: List[Transaction] = []
        for raw_transaction in raw_sequence:

            items: List[Item] = []
            for raw_item in raw_transaction:
                items.append(Item(raw_item))
            if len(items) == 0:
                break
            transactions.append(Transaction(items))

        if len(transactions) == 0:
            break
        result_sequences.append(Sequence(transactions))

    return result_sequences
