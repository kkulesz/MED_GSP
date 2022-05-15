import sys

from gsp import GSP
from main import from_file
import consts

if __name__ == '__main__':
    seqs = from_file('data.txt')
    num_of_seqs = len(seqs)

    # set these values, so we get not generalized version
    consts.MAX_GAP = sys.maxsize
    consts.MIN_GAP = 0
    consts.WINDOW_SIZE = 0

    result = GSP.run(
        seqs,
        min_supp=1,
        min_return_length=1
    )
    with_relative_support = [(v[0], v[1]/num_of_seqs) for v in result]

    print('=' * 50)
    print("RESULT")
    for i, r in enumerate(with_relative_support):
        print(i, ' ', r)
