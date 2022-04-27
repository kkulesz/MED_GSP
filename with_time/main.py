from gsp import GSP
from utils_classes import *


def convert_list(raw_sequences):
    result_sequences: List[Sequence] = []
    for raw_sequence in raw_sequences:
        transactions: List[Transaction] = []
        for raw_transaction in raw_sequence:
            time = raw_transaction[0]
            items: Set[Item] = set()
            for raw_item in raw_transaction[1]:
                items.add(Item(raw_item))
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
            (2, [1, 2, 3, 4]), (10, [1, 5])
        ],
        [
            (5, [1, 2, 3])
        ],
        [
            (5, [1, 2])
        ],
        [
            (5, [1, 2, 3])
        ]
    ]
    data = convert_list(input_seqs)
    result = GSP.run(
        data,
        min_supp=3,
        window_size=20,
        min_gap=10,
        max_gap=100,
        min_return_length=3
    )

    print('~' * 100)
    print('RESULT:')
    for r in result:
        print(r)

    # print(SequenceCandidate([Element([Item(2), Item(1), Item(2)]), Element([Item(3)])]))
