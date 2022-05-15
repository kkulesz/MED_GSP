from gsp import GSP
from main import from_file

if __name__ == '__main__':
    seqs = from_file('data.txt')
    num_of_seqs = len(seqs)

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
