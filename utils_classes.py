from __future__ import annotations
from typing import List, Set, Optional, Tuple, Dict
from dataclasses import dataclass
from collections import OrderedDict
import collections
import uuid

from consts import MAX_GAP, MIN_GAP, WINDOW_SIZE


@dataclass
class Item:
    data: any

    def __repr__(self):
        return f"{self.data}"

    def __str__(self):
        return f"{self.data}"

    def __hash__(self):
        return hash(self.data)

    # def __eq__(self, other):
    #     return self.data == other.data

    def __lt__(self, other):
        return self.data < other.data


@dataclass
class Transaction:
    time: int
    items: List[Item]

    def __init__(self, time, items: List[Item]):
        items.sort()
        # TODO: remove duplicates?
        self.time = time
        self.items = items

    def __lt__(self, other):
        return self.time < other.time

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        return self.items[idx]


@dataclass
class Sequence:
    transactions: List[Transaction]

    def __init__(self, transactions: List[Transaction]):
        transactions.sort()
        self.transactions = transactions

    def __len__(self):
        return sum(len(t) for t in self.transactions)

    def __getitem__(self, idx) -> Tuple[Item, int]:
        for tr in self.transactions:
            if idx < len(tr):
                return tr[idx], tr.time
            idx = idx - len(tr)
        raise ("invalid index")


# =======================================================
@dataclass
class Window:
    since: int
    to: int


@dataclass
class Element:
    items: List[Item]

    def __init__(self, items: List[Item]):
        """ sort and remove duplicates, so adding (b, b, a) and (a, b) gives the same result"""
        items.sort()
        without_duplicates = list(OrderedDict.fromkeys(items))
        self.items = without_duplicates

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        s = [str(i) for i in self.items]
        return f"({', '.join(s)})"

    def __str__(self):
        s = [str(i) for i in self.items]
        return f"({', '.join(s)})"

    def __hash__(self):
        return hash(tuple(self.items))

    def without_first(self) -> Optional[Element]:
        without_first = self.items[1:]
        if len(without_first) == 0:
            return None
        else:
            return Element(without_first)

    def without_last(self) -> Optional[Element]:
        without_last = self.items[:-1]
        if len(without_last) == 0:
            return None
        else:
            return Element(without_last)


@dataclass
class SequenceCandidate:
    elements: List[Element]

    def __repr__(self):
        return f"{self.elements}"

    def __eq__(self, other: SequenceCandidate):
        return collections.Counter(self.elements) == collections.Counter(other.elements)

    def __len__(self):
        return sum(len(t) for t in self.elements)

    def __hash__(self):
        return hash(tuple(self.elements))

    def only(self) -> Item:
        assert len(self) == 1
        return self.elements[0].items[0]

    def without_first(self) -> Optional[SequenceCandidate]:
        first_without_first = self.elements[0].without_first()
        if first_without_first is None and len(self) == 1:
            return None
        elif first_without_first is None:
            return SequenceCandidate(self.elements[1:])
        else:
            without_first = [first_without_first] + self.elements[1:]
            return SequenceCandidate(without_first)

    def without_last(self) -> Optional[SequenceCandidate]:
        last_without_last = self.elements[-1].without_last()
        if last_without_last is None and len(self) == 1:
            return None
        elif last_without_last is None:
            return SequenceCandidate(self.elements[:-1])
        else:
            without_last = self.elements[:-1] + [last_without_last]
            return SequenceCandidate(without_last)

    @staticmethod
    def generate_all_possible(
            first: SequenceCandidate,
            second: SequenceCandidate
    ) -> List[SequenceCandidate]:
        left = first.without_first()
        right = second.without_last()

        if left is None:
            assert right is None
            within_same = SequenceCandidate(  # (a) + (b) => (ab)
                [Element([first.only(), second.only()])]
            )
            separate = SequenceCandidate([  # (a) + (b) => (a)(b)
                Element([first.only()]),
                Element([second.only()])
            ])
            return [within_same, separate]

        if left == right:
            if len(second.elements[-1].items) == 1:
                new_elements = first.elements + [second.elements[-1]]
                return [SequenceCandidate(new_elements)]
            else:
                first_last_element = first.elements[-1]
                second_last_item = second.elements[-1].items[-1]
                new_last_element = Element(first_last_element.items + [second_last_item])
                new_elements = first.elements[:-1] + [new_last_element]
                return [SequenceCandidate(new_elements)]

        return []  # cannot be generated

    def generate_contiguous_subsequences(self) -> List[SequenceCandidate]:
        subsequences = set()
        for i in range(len(self.elements)):
            if i != 0 and i != len(self.elements) - 1:
                if len(self.elements[i]) < 2:
                    break
            for j in range(len(self.elements[i])):
                copied = self.elements[i].items.copy()
                copied.pop(j)
                if len(copied) == 0:
                    ss_trans = self.elements[0:i] + self.elements[i + 1:]
                else:
                    ss_trans = self.elements[0:i] + [Element(copied)] + self.elements[i + 1:]

                subsequences.add(SequenceCandidate(ss_trans))
        return list(subsequences)

    def flatten(self) -> List[Item]:
        result = []
        for el in self.elements:
            for it in el.items:
                result.append(it)
        return result

    def is_supported_by(self, data_sequence: Sequence) -> bool:
        item_to_times_dict: Dict[Item, List[int]] = {}
        for idx in range(len(data_sequence)):
            item, its_time = data_sequence[idx]
            if item in item_to_times_dict:
                item_to_times_dict[item].append(its_time)
            else:
                item_to_times_dict[item] = [its_time]

        find_after = -1
        found: List[Tuple[Element, Window]] = []
        next_element: Element = self.elements[0]
        while True:
            window = self.find_element(next_element, item_to_times_dict, find_after)
            if window is None:
                return False  # No element found after specified time => sequence DOES NOT support candidate

            if len(found) == 0 or found[-1][1].to - window.since < MAX_GAP:
                # forward pass
                found.append((next_element, window))
                find_after = window.to + MIN_GAP + 1
                if len(found) == len(self.elements):
                    return True  # All elements were found and they meet GSP's restrictions => sequence DOES support candidate
                next_element = self.elements[len(found)]
            else:
                # backward pass
                last = found[-1]
                next_element = last[0]
                find_after = window.to - MAX_GAP + 1
                found = found[0: -1]

    def find_element(
            self,
            element: Element,
            item_to_times_dict: Dict[Item, List[int]],
            find_after: int
    ) -> Optional[Window]:
        to_find: Set[Item] = set(element.items)
        found: List[Tuple[Item, int]] = []
        while len(to_find) != 0:
            item = to_find.pop()
            if item not in item_to_times_dict:
                return None
            times = item_to_times_dict[item]
            time = next(filter(lambda t: t >= find_after, times), None)
            if time is None:
                return None

            still_in_window, not_in_window_anymore = [], []
            for x in found:
                x_time = x[1]
                if time-WINDOW_SIZE <= x_time <= time+WINDOW_SIZE:
                    still_in_window.append(x)
                else:
                    not_in_window_anymore.append(x)

            found = still_in_window + [(item, time)]
            items_again_to_find = list(map(lambda x: x[0], not_in_window_anymore))
            to_find.update(items_again_to_find)
            find_after = max(find_after, time - WINDOW_SIZE)

        times = list(map(lambda x: x[1], found))
        return Window(min(times), max(times))



        # for element in self.elements:
        #     window = self.find_element_after(element, item_to_times_dict, find_after)
        #     if window is None:
        #         return False
