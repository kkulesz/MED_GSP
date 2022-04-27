from typing import List, Tuple
from utils_classes import *
from utils import *
from datasets import *


class GSP:
    @staticmethod
    def run(sequences: List[Sequence], min_supp: int, min_return_length: int = 2) -> List[Sequence]:
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
            previous_candidates = candidates

            # 3.1
            generated_candidates = GSP._generate_candidates(candidates)
            # print(f"generated: {len(generated_candidates)}")
            pruned = GSP._prune_candidates(previous_candidates, generated_candidates)
            # print(f"pruned: {len(pruned)}")
            # 3.2
            counted = GSP._count_candidates(sequences, pruned)
            # print(f"counted: {len(counted)}")
            candidates = [v[0] for v in counted if v[1] >= min_supp]
        return candidates_to_return

    @staticmethod
    def _first_pass(sequences: List[Sequence]) -> List[Tuple[Item, int]]:
        """
        Counts number of item occurrences in given sequences.
        E.g.
        for input: [
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
    def _generate_candidates(previous: List[Sequence]) -> List[Sequence]:
        result = set()
        for i in range(len(previous)):
            for j in range(len(previous)):
                generated = Sequence.generate_if_possible(previous[i], previous[j])
                for g in generated:
                    if g not in result:
                        result.add(g)

        return list(result)

    @staticmethod
    def _prune_candidates(
            previous_candidates: List[Sequence],
            new_candidates: List[Sequence]
    ) -> List[Sequence]:
        result = []
        previous_candidates_set = set(previous_candidates)
        for candidate in new_candidates:
            subsequences = candidate.generate_subsequences()
            if all(previous_candidates_set.__contains__(ss) for ss in subsequences):
                result.append(candidate)
        return result

    @staticmethod
    def _count_candidates(input_sequences: List[Sequence], candidates: List[Sequence]) -> List[Tuple[Sequence, int]]:
        candidates_with_support: List[Tuple[Sequence, int]] = []
        for candidate in candidates:
            occurrences = sum(1 for s in input_sequences if s.check_if_contains(candidate))
            if occurrences > 0:
                candidates_with_support.append((candidate, occurrences))

        return candidates_with_support


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

    # data = one()
    data = data[: 100]
    result = GSP.run(data, min_supp=4, min_return_length=2)

    print(result)
