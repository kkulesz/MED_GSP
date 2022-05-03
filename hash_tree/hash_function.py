from utils_classes import Item
from consts import MODULO_VALUE


def hash_function(item: Item) -> int:
    return item.data % MODULO_VALUE
