from itertools import groupby
from typing import List
import statistics

from data_classes.item import Item
from data_classes.sequence import Sequence, Transaction


def convert_list(raw_sequences) -> List[Sequence]:
    result_sequences: List[Sequence] = []
    for raw_sequence in raw_sequences:
        transactions: List[Transaction] = []
        for raw_transaction in raw_sequence:
            time = raw_transaction[0]
            items: List[Item] = []
            for raw_item in raw_transaction[1]:
                items.append(Item(raw_item))
            if len(items) == 0:
                break
            transactions.append(Transaction(time, items))

        if len(transactions) == 0:
            break
        result_sequences.append(Sequence(transactions))

    return result_sequences


def from_file(filepath):
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
        transaction_time = 0
        for raw_t in raw_transactions_ints:
            items = list(map(lambda i: Item(i), raw_t))
            transaction_time += 5
            transactions.append(Transaction(transaction_time, items))
        sequences.append(Sequence(transactions))

    return sequences


def calculate_mean_length(sequences: List[Sequence]) -> float:
    number_of_sequences = len(sequences)
    cumulative_length = 0
    for s in sequences:
        cumulative_length += len(s)

    return cumulative_length / number_of_sequences


def calculate_median(sequences: List[Sequence]) -> float:
    lengths = []
    for s in sequences:
        lengths.append(len(s))

    return statistics.median(lengths)
