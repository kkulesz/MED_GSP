from typing import List, Tuple
from utils_classes import *
from utils import *


class GSP:
    @staticmethod
    def run(sequences: List[Sequence], min_supp: int, min_return_length=2) -> List[Sequence]:
        first_pass_candidates = GSP._first_pass(sequences)
        after_first_pass = [v[0] for v in first_pass_candidates if v[1] >= min_supp]

        candidates_to_return = []
        length_counter = 1
        candidates = list(map(lambda item: Sequence([Transaction([item])]), after_first_pass))
        while len(candidates) != 0:
            print(f"After {length_counter}. pass:")
            print(candidates)
            print("=" * 50)
            if length_counter >= min_return_length:
                candidates_to_return += candidates
            length_counter += 1

            generated_candidates = GSP._generate_candidates(candidates)
            counted = GSP._count_candidates(sequences, generated_candidates)
            candidates = [v[0] for v in counted if v[1] >= min_supp]

        return candidates_to_return

    @staticmethod
    def _first_pass(sequences: List[Sequence]) -> List[Tuple[Item, int]]:
        """
        Counts number of item occurrences in given sequences.
        E.g. [
                - [A,B], [A, B, C]
                - [A]
            ]

            returns (A: 2), (B: 1), (C: 1)
        """
        items_support_dict = {}  # TODO: possible to assign type?
        for seq in sequences:
            for tran in seq.transactions:
                visited = set()
                for item in tran.items:
                    if item in visited:
                        continue
                    visited.add(item)

                    if item not in items_support_dict:
                        items_support_dict[item] = 1
                    else:
                        items_support_dict[item] += 1

        return [(item, supp_val) for item, supp_val in items_support_dict.items()]

    @staticmethod
    def _generate_candidates(previous_candidates: List[Sequence]) -> List[Sequence]:
        # TODO
        return []

    @staticmethod
    def _count_candidates(input_sequences: List[Sequence], candidates: List[Sequence]) -> List[Tuple[Sequence, int]]:
        # TODO
        return []


if __name__ == '__main__':
    input_seqs = [
        [
            [1, 2], [3], [4]
        ],
        [
            [1], [2]
        ],
        [
            [1, 2, 3]
        ]
    ]
    converted = convert(input_seqs)
    GSP.run(converted, min_supp=2, min_return_length=1)
