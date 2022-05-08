from __future__ import annotations
from typing import List, Optional, Tuple
from dataclasses import dataclass
import uuid

from data_classes.item import Item


@dataclass
class Transaction:
    time: int
    items: List[Item]

    def __init__(self, time, items: List[Item]):
        items.sort()
        # TODO: remove duplicates?
        self.time = time
        self.items = items

    def __repr__(self):
        s = [str(i) for i in self.items]
        return f"({self.time}: {', '.join(s)})"

    def __str__(self):
        s = [str(i) for i in self.items]
        return f"({self.time}: {', '.join(s)})"

    def __hash__(self):
        return hash(tuple(self.items)) + hash(self.time)

    def __lt__(self, other):
        return self.time < other.time

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        return self.items[idx]


@dataclass
class Sequence:
    transactions: List[Transaction]
    id: uuid  # so hashing gives different values for the same transaction set

    def __init__(self, transactions: List[Transaction]):
        transactions.sort()
        self.transactions = transactions
        self.id = uuid.uuid1()

    def __repr__(self):
        s = [str(i) for i in self.transactions]
        return f"({', '.join(s)})"

    def __str__(self):
        s = [str(i) for i in self.transactions]
        return f"({', '.join(s)})"

    def __hash__(self):
        return hash(tuple(self.transactions)) + hash(self.id)

    def __len__(self):
        return sum(len(t) for t in self.transactions)

    def __getitem__(self, idx) -> Tuple[Item, int]:
        for tr in self.transactions:
            if idx < len(tr):
                return tr[idx], tr.time
            idx = idx - len(tr)
        raise Exception(f"Invalid index. length={len(self)}, index={idx}")

    def without_item(self, item: Item, its_time: int) -> Optional[Sequence]:
        found = False
        new_transactions = []
        for t in self.transactions:
            new_items = []
            for it in t.items:
                if it == item and t.time == its_time and not found:
                    found = True
                    continue
                new_items.append(it)
            if len(new_items) != 0:
                new_transactions.append(Transaction(t.time, new_items))

        return Sequence(new_transactions)
