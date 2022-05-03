from abc import ABC, abstractmethod

from utils_classes import SequenceCandidate


class Node(ABC):
    def __init__(self, depth):
        self.depth = depth

    @abstractmethod
    def add(self, candidate: SequenceCandidate):
        pass

    @abstractmethod
    def print(self):
        pass
