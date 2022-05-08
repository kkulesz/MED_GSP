from __future__ import annotations
from typing import List, Set, Tuple

from hash_tree.interior_node import InteriorNode
from hash_tree.leaf_node import LeafNode
from data_classes.sequence_candidate import SequenceCandidate
from data_classes.sequence import Sequence


class HashTree:
    def __init__(self, candidates: List[SequenceCandidate]):
        self.root: InteriorNode = InteriorNode(depth=0)
        self.candidates: Set[SequenceCandidate] = set()
        self._create(candidates)

    def count_support(
            self,
            data_sequences: List[Sequence],
            supportive_sequences: Set[Sequence]
    ) -> List[Tuple[SequenceCandidate, int]]:
        supports = dict.fromkeys(self.candidates, 0)
        for data_seq in data_sequences:
            possible_leaves: Set[LeafNode] = set()
            self.root.start_gathering_leaves(data_seq, possible_leaves)
            for leaf in possible_leaves:
                for candidate in leaf.candidates:
                    if candidate.is_supported_by(data_seq):
                        supportive_sequences.add(data_seq)
                        supports[candidate] += 1

        return [(candidate, supp_val) for candidate, supp_val in supports.items()]

    def _create(self, candidates: List[SequenceCandidate]):
        for c in candidates:
            if c not in self.candidates:
                self.root.add(c)
                self.candidates.add(c)

    def print(self):
        self.root.print()

