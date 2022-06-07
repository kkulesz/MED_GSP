import time
import pandas as pd

import utils
from consts import MIN_SUPPORT
from gsp import GSP

file_1 = 'BMS1_spmf.txt'
file_2 = 'MT745584_SPMF.txt'

if __name__ == '__main__':
    # input_seqs = [
    #     [
    #         (3, [1, 2]), (4, [3]), (12, [4])
    #     ],
    #     [
    #         (3, [1, 2]), (4, [3]), (12, [4])
    #     ],
    #     [
    #         (3, [1, 2]), (1000, [3])
    #     ],
    #     [
    #         (1, [1])
    #     ]
    # ]
    # data = utils.convert_list(input_seqs)
    used_file = file_1
    df = pd.DataFrame.from_dict({
        'Number of sequences': [],
        'Mean length': [],
        'Median': [],
        'Execution time': []
    })
    for i in [i for i in range(1, 11)]:
        max_number_of_sequences = 1000 * i
        data = utils.from_file(f'data/{used_file}')
        data = data[0:max_number_of_sequences]

        number_of_sequences = len(data)
        mean = utils.calculate_mean_length(data)
        median = utils.calculate_median(data)

        startTime = time.time()
        result = GSP.run(
            data,
            min_supp=MIN_SUPPORT,
            min_return_length=1
        )
        executionTime = (time.time() - startTime)

        # print('RESULT:')
        # for r in result:
        #     print(r)
        print('-'*100)
        print(f'Number of sequences: {number_of_sequences}')
        print(f'Mean length: {mean}')
        print(f'Median: {median}')
        print('Execution time: {:,.3f}s'.format(executionTime))
        df = df.append({
            'Number of sequences': number_of_sequences,
            'Mean length': mean,
            'Median': median,
            'Execution time': executionTime
        }, ignore_index=True)
    df.to_csv(f'results-{used_file}.csv')
