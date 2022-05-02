import time

from gsp import GSP
from utils_classes import *


def convert_list(raw_sequences):
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
    print('Execution time in seconds: ' + str(executionTime))

    # print(SequenceCandidate([Element([Item(2), Item(1), Item(2)]), Element([Item(3)])]))
