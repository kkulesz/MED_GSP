from typing import List, Optional, Set

from data_classes.sequence_candidate import SequenceCandidate
from data_classes.sequence import Sequence
from data_classes.item import Item
from hash_tree.hash_function import hash_function
from hash_tree.node import Node
from hash_tree.leaf_node import LeafNode
from consts import MODULO_VALUE, WINDOW_SIZE, MAX_GAP


class InteriorNode(Node):
    def __init__(self, depth):
        super().__init__(depth)
        self.children: List[Optional[Node]] = [None] * MODULO_VALUE

    def add(self, candidate: SequenceCandidate):
        flattened = candidate.flatten()
        hash_value = hash_function(flattened[self.depth])
        node = self.children[hash_value]
        if isinstance(node, LeafNode):
            if node.exceeds_after_add(candidate) and len(flattened) > self.depth + 1:
                new_interior = InteriorNode(self.depth + 1)
                for c in node.candidates:
                    new_interior.add(c)
                new_interior.add(candidate)
                self.children[hash_value] = new_interior
            else:
                node.add(candidate)

        elif isinstance(node, InteriorNode):
            node.add(candidate)

        else:
            new_leaf = LeafNode(self.depth + 1)
            new_leaf.add(candidate)
            self.children[hash_value] = new_leaf

    def start_gathering_leaves(self, data_seq, supports: Set[LeafNode]):
        for idx in range(len(data_seq)):
            it, its_time = data_seq[idx]
            hash_value = hash_function(it)
            node = self.children[hash_value]
            if isinstance(node, InteriorNode):
                node.gather_leaves(data_seq, it, its_time, supports)
            elif isinstance(node, LeafNode):
                supports.add(node)

    def gather_leaves(
            self,
            data_seq: Sequence,
            item: Item,
            time: int,
            supports: Set[LeafNode]
    ):
        data_seq = data_seq.without_item(item, time)  # so we do not hash with the same item twice
        for idx in range(len(data_seq)):
            it, its_time = data_seq[idx]
            if time - WINDOW_SIZE <= its_time <= time + max(WINDOW_SIZE, MAX_GAP):
                hash_value = hash_function(it)
                node = self.children[hash_value]
                if isinstance(node, InteriorNode):
                    node.gather_leaves(data_seq, it, its_time, supports)
                elif isinstance(node, LeafNode):
                    supports.add(node)

    def print(self):
        print("  " * self.depth + f"Interior({self.depth}):")
        for n in self.children:
            if isinstance(n, Node):
                n.print()
