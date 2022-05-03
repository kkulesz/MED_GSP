import time
from itertools import groupby

from consts import MAX_NUMBER_OF_SEQUENCES
from gsp import GSP
from utils_classes import *


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


file_1 = 'data/BMS1_spmf.txt'
file_2 = 'data/MT745584_SPMF.txt'

if __name__ == '__main__':
    input_seqs = [
        [
            (3, [1, 2]), (4, [1]), (12, [1])
        ],
        [
            (3, [1, 2]), (4, [1]), (12, [1])
        ],
        [
            (3, [1, 2]), (4, [1])
        ]
    ]
    data = convert_list(input_seqs)
    data = from_file(file_2)
    data = data[0:MAX_NUMBER_OF_SEQUENCES]

    startTime = time.time()
    result = GSP.run(
        data,
        min_supp=2,
        min_return_length=3
    )
    executionTime = (time.time() - startTime)

    print('RESULT:')
    for r in result:
        print(r)
    print('Execution time: {:,.3f}s'.format(executionTime))
