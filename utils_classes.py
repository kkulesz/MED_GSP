from typing import List, Set
from dataclasses import dataclass
import collections
import uuid

"""
<{a,b}, {c}, {e,f}>

Sequence:       <{a,b}, {c}, {e,f}>
Transaction:    {a,b,c}
Item:           a
"""


@dataclass(frozen=True)
class Item:
    data: any


@dataclass(frozen=True)
class Transaction:
    items: List[Item]

    def __eq__(self, another):
        raise

    def __hash__(self):
        raise

    def __repr__(self):
        return f"{self.items}"

    def __len__(self):
        raise

    def check_if_contain(self, other) -> bool:
        pass


@dataclass(frozen=True)
class Sequence:
    transactions: List[Transaction]  # TODO: maybe set?

    def __eq__(self, another):
        raise

    def __repr__(self):
        return f"{self.transactions}"

    def __hash__(self):
        raise
        # return hash(tuple(map(tuple, self.transactions)))

    def __len__(self):
        raise

    def check_if_contain(self, other_sequence) -> bool:
        pass


@dataclass(frozen=True)
class Record:
    sequence: Sequence
    id: uuid
