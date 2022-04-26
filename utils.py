from typing import List
from utils_classes import *


def convert(raw_sequences):
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
