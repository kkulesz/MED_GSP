from dataclasses import dataclass


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
