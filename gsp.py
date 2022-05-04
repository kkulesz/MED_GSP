from typing import List, Dict, Set

from utils_classes import Sequence, SequenceCandidate, Element, Item
from hash_tree.hash_tree import HashTree


class GSP:
    @staticmethod
    def run(
            data_sequences: List[Sequence],
            min_supp: int,
            min_return_length: int = 2
    ):
        candidates = GSP._first_pass(data_sequences, min_supp)

        candidate_length = 1
        result = []
        while len(candidates) != 0:
            candidate_length += 1
            print('=' * 100 + f'\nIteration nr {candidate_length}.:')
            print(f'Number of candidates: {len(candidates)}')
            previous_candidates = candidates

            # 3.1 Candidate Generation
            generated = GSP._generate_candidates(previous_candidates)
            print(f'Number of generated candidates: {len(generated)}')
            pruned = GSP._prune_candidates(previous_candidates, generated)
            print(f'Number of generated candidates after pruning: {len(pruned)}')

            # 3.2 Counting Candidates
            hash_tree = HashTree(pruned)
            # hash_tree.print()

            supportive_sequences_set = set()
            candidates_with_support = hash_tree.count_support(data_sequences, supportive_sequences_set)
            data_sequences = list(supportive_sequences_set)
            # print(f'With support = {candidates_with_support}')
            print(f'Number of supportive sequences: {len(data_sequences)}')
            # for s in data_sequences:
            #     print(f'   {s}')

            candidates = [v[0] for v in candidates_with_support if v[1] >= min_supp]
            if candidate_length >= min_return_length:
                result.append(candidates)
        return result

    @staticmethod
    def _first_pass(
            data_sequences: List[Sequence],
            min_support: int
    ) -> List[SequenceCandidate]:
        item_support: Dict[Item, int] = {}
        for seq in data_sequences:
            visited = set()
            for tran in seq.transactions:
                for item in tran.items:
                    if item in visited:
                        continue
                    visited.add(item)
                    if item not in item_support:
                        item_support[item] = 1
                    else:
                        item_support[item] += 1

        tuples = [(pos, supp_val) for pos, supp_val in item_support.items()]
        items_with_min_support = [v[0] for v in tuples if v[1] >= min_support]
        return list(map(lambda it: SequenceCandidate([Element([it])]), items_with_min_support))

    @staticmethod
    def _generate_candidates(
            previous: List[SequenceCandidate]
    ) -> List[SequenceCandidate]:
        result: Set[SequenceCandidate] = set()
        for i in range(len(previous)):
            for j in range(len(previous)):
                generated = SequenceCandidate.generate_all_possible(previous[i], previous[j])
                for g in generated:
                    if g not in result and len(g) > len(previous[i]):
                        result.add(g)

        return list(result)

    @staticmethod
    def _prune_candidates(
            previous_candidates: List[SequenceCandidate],
            new_candidates: List[SequenceCandidate]
    ) -> List[SequenceCandidate]:
        result: List[SequenceCandidate] = []
        previous_candidates_set: Set[SequenceCandidate] = set(previous_candidates)
        for candidate in new_candidates:
            subsequences = candidate.generate_contiguous_subsequences()
            if all(previous_candidates_set.__contains__(ss) for ss in subsequences):
                result.append(candidate)
        return result
