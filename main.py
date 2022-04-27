from utils import *
from datasets import *
from gsp import GSP

file_1 = 'BMS1_spmf.txt'
file_2 = 'MT745584_SPMF.txt'

if __name__ == '__main__':
    input_seqs = [
        [
            [1, 2, 3, 4], [5]
        ],
        [
            [1, 2, 3, 4], [5]
        ],
        [
            [1, 2, 3], [5]
        ],
        [
            [1], [5]
        ],
        [
            [1], [5]
        ]
    ]
    data = convert(input_seqs)

    # data = read_and_convert(f"data/{file_2}")
    # data = data[:100]
    result = GSP.run(data, min_supp=3, min_return_length=3)

    print('~'*100)
    print('RESULT:')
    for r in result:
        print(r)
