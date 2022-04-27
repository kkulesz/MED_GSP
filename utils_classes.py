from __future__ import annotations
from typing import List, Set, Optional
from dataclasses import dataclass
import collections
import uuid

"""
Low level classes so implementing algorithm is a little bit more abstract


<{a,b}, {c}, {e,f}>

Sequence:       <{a,b}, {c}, {e,f}>
Transaction:    {a,b,c}
Item:           a
"""


@dataclass(frozen=True)
class Item:
    data: any

    def __repr__(self):
        return f"{self.data}"

    def __lt__(self, other):
        return self.data < other.data


@dataclass()
class Transaction:
    items: List[Item]

    def __init__(self, its: List[Item]):
        its.sort()
        self.items = its

    def __eq__(self, another):
        return collections.Counter(self.items) == collections.Counter(another.items)

    def __hash__(self):
        return hash(tuple(self.items))

    def __repr__(self):
        return f"{self.items}"

    def __len__(self):
        return len(self.items)

    def check_if_contains(self, other: Transaction) -> bool:
        l1 = self.items.copy()
        l2 = other.items.copy()
        for el in l2:
            if el in l1:
                l1.remove(el)
            else:
                return False
        return True

    def without_first(self) -> Optional[Transaction]:
        without_first = self.items[1:]
        if len(without_first) == 0:
            return None
        else:
            return Transaction(without_first)

    def without_last(self) -> Optional[Transaction]:
        without_last = self.items[:-1]
        if len(without_last) == 0:
            return None
        else:
            return Transaction(without_last)


@dataclass(frozen=True)
class Sequence:
    transactions: List[Transaction]

    def __eq__(self, another):
        return self.transactions == another.transactions

    def __repr__(self):
        return f"{self.transactions}"

    def __hash__(self):
        return hash(tuple(self.transactions))

    def __len__(self):
        return sum(len(t) for t in self.transactions)

    def check_if_contains(self, other_sequence) -> bool:
        found = 0
        for i in range(len(self.transactions)):
            if self.transactions[i].check_if_contains(other_sequence.transactions[found]):
                found += 1
            if found == len(other_sequence.transactions):
                return True
            if len(self.transactions) < i + (len(other_sequence) - found):
                break
        return False

    def _without_first(self) -> Optional[Sequence]:
        first_without_first = self.transactions[0].without_first()
        if first_without_first is None and len(self) == 1:
            return None
        elif first_without_first is None:
            return Sequence(self.transactions[1:])
        else:
            without_first = [first_without_first] + self.transactions[1:]
            return Sequence(without_first)

    def _without_last(self) -> Optional[Sequence]:
        last_without_last = self.transactions[-1].without_last()
        if last_without_last is None and len(self) == 1:
            return None
        elif last_without_last is None:
            return Sequence(self.transactions[:-1])
        else:
            without_last = self.transactions[:-1] + [last_without_last]
            return Sequence(without_last)

    def only(self) -> Item:
        assert len(self) == 1
        return self.transactions[0].items[0]

    def generate_subsequences(self) -> List[Sequence]:
        subsequences = set()
        for i in range(len(self.transactions)):
            if i != 0 and i != len(self.transactions) - 1:
                if len(self.transactions[i]) < 2:
                    break
            for j in range(len(self.transactions[i])):
                copied = self.transactions[i].items.copy()
                copied.pop(j)
                if len(copied) == 0:
                    ss_trans = self.transactions[0:i] + self.transactions[i + 1:]
                else:
                    ss_trans = self.transactions[0:i] + [Transaction(copied)] + self.transactions[i + 1:]

                subsequences.add(Sequence(ss_trans))
        return list(subsequences)

    @staticmethod
    def generate_if_possible(first: Sequence, second: Sequence) -> List[Sequence]:
        first_without_first = first._without_first()
        second_without_last = second._without_last()

        if first_without_first is None:  # for i == 2
            assert second_without_last is None
            within_same = Sequence(  # (a) + (b) => (ab)
                [Transaction([
                    first.only(), second.only()
                ])])
            separate = Sequence([  # (a) + (b) => (a)(b)
                Transaction([first.only()]),
                Transaction([second.only()])
            ])
            return [within_same, separate]

        if first_without_first == second_without_last:  # for i > 2
            if len(second.transactions[-1].items) == 1:
                new_transactions = first.transactions + [second.transactions[-1]]
                return [Sequence(new_transactions)]
            else:
                first_last_transaction = first.transactions[-1]
                second_last_item = second.transactions[-1].items[-1]
                new_last_transaction = Transaction(first_last_transaction.items + [second_last_item])
                new_transactions = first.transactions[:-1] + [new_last_transaction]
                return [Sequence(new_transactions)]

        return []


# @dataclass(frozen=True)
# class TransactionWindows:
#     transactions: List[Transaction]
