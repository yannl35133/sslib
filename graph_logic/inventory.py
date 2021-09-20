from typing import NewType, Union, Optional, Tuple
from enum import IntEnum

from .item_types import INVENTORY_ITEMS


ItemName = NewType("ItemName", str)


ITEM_COUNTS = {i: INVENTORY_ITEMS.count(i) for i in INVENTORY_ITEMS}


def extended_item_generator():
    for item, n in ITEM_COUNTS.items():
        if n == 1:
            yield item
        else:
            for i in range(n):
                yield f"{item} #{i}"


class MetaGetItem(type):
    def __getitem__(self, arg):
        return self.getitem(arg)


class EXTENDED_ITEM(int, metaclass=MetaGetItem):
    items_list = list(extended_item_generator())
    # Events must be added here

    @classmethod
    def getitem(cls, name):
        return cls.items_list.index(name)


class Inventory:
    bitset: int

    def __init__(self, v: Optional[Union[int, Tuple[ItemName, int]]] = None):
        if v is None:
            self.bitset = 0
        elif isinstance(v, int):
            self.bitset = v
        elif isinstance(v, tuple):  # Item, count
            item, count = v
            assert count <= ITEM_COUNTS[item]
            if ITEM_COUNTS[item] == 1:
                self.bitset = 1 << (EXTENDED_ITEM[item])
            else:
                for i in range(count):
                    self.bitset |= 1 << EXTENDED_ITEM[f"{item} #{i}"]

    def __getitem__(self, index):
        if isinstance(index, EXTENDED_ITEM):
            return bool(self.bitset | (1 << index))
        # elif isinstance(index, ItemName):
        #     indices = [
        #         EXTENDED_ITEM[f"{index} #{i}"] for i in range(ITEM_COUNTS[index])
        #     ]
        #     return sum(int(self[i]) for i in indices)
        else:
            raise ValueError

    def __or__(self, other):
        if isinstance(other, EXTENDED_ITEM):
            return Inventory(self.bitset | (1 << other))
        elif isinstance(other, Inventory):
            return Inventory(self.bitset | other.bitset)
        else:
            raise ValueError

    def __and__(self, other):
        if isinstance(other, Inventory):
            return Inventory(self.bitset & other.bitset)
        else:
            raise ValueError

    def __le__(self, other):
        """Define inclusion"""
        return self.bitset | other.bitset == other.bitset

    def add(self, item):
        if isinstance(item, EXTENDED_ITEM):
            return self | item
        elif isinstance(item, str):
            for i in range(ITEM_COUNTS[item]):
                if not self[(item_bit := EXTENDED_ITEM[f"{item} #{i}"])]:
                    return self | item_bit
        raise ValueError

    def remove(self, item):
        if isinstance(item, EXTENDED_ITEM):
            return Inventory(self.bitset & ~(1 << item))
        elif isinstance(item, str):
            for i in reversed(range(ITEM_COUNTS[item])):
                if self[(item_bit := EXTENDED_ITEM[f"{item} #{i}"])]:
                    return Inventory(self.bitset & ~(1 << item_bit))
        raise ValueError

    @staticmethod
    def simplify_invset(argset):
        def gen():
            for bitset in argset:
                for bitset2 in argset:
                    if bitset2 <= bitset and bitset2 != bitset:
                        break
                else:
                    yield bitset

        return set(gen())

    def all_owned_unique_items(self):
        return set(
            (
                (v := item.name)[: v.index("#") - 1]
                for item in EXTENDED_ITEM
                if self[item]
            )
        )


class RevInventory(Inventory):
    def __init__(self, v=-1):
        super().__init__(v)
