from typing import NewType, Union, Optional, Tuple
from enum import IntEnum
from functools import cache

from options import OPTIONS_LIST
from .constants import *

ItemName = NewType("ItemName", str)


def extended_item_generator():
    yield from ["Day", "Night"]  # Dummy events, will be removed from the requirements
    yield from ["Banned", "Everything"]  # Technical dummy events

    yield from INVENTORY_ITEMS

    yield from LOGIC_OPTIONS

    for option in OPTIONS_LIST:
        if option["name"].startswith("Enabled Tricks"):
            for trick in option["choices"]:
                yield f"{trick} Trick"


class MetaContainer(type):
    def __getitem__(self, arg):
        return self.getitem(arg)

    def __len__(self):
        return self.len()

    def __iter__(self):
        return self.iter()


class EXTENDED_ITEM(int, metaclass=MetaContainer):
    items_list = list(extended_item_generator())

    @classmethod
    def day_bit(cls):
        return cls["Day"]

    @classmethod
    def night_bit(cls):
        return cls["Night"]

    @classmethod
    def banned_bit(cls):
        return cls["Banned"]

    @classmethod
    def everything_bit(cls):
        return cls["Everything"]

    @classmethod
    def items(cls):
        for i in range(len(cls)):
            yield cls(i)

    @classmethod
    def len(cls):
        return len(cls.items_list)

    @classmethod
    def iter(cls):
        return iter(cls.items_list)

    @classmethod
    def getitem(cls, name):
        return cls(cls.items_list.index(name))

    @classmethod
    def get_item_name(cls, i):
        return cls.items_list[i]


class Inventory:
    bitset: int

    def __init__(
        self,
        v: Optional[Union[int, Tuple[ItemName, int]]] = None,
        intset: Optional[Set[EXTENDED_ITEM]] = None,
    ):
        if intset is not None:
            assert isinstance(v, int)
            self.bitset = v
            self.intset = intset
        if v is None:
            self.bitset = 0
            self.intset = set()
        elif isinstance(v, set):
            bitset = 0
            for item in v:
                bitset += 1 << item
            self.intset = v
            self.bitset = bitset
        elif isinstance(v, EXTENDED_ITEM):
            self.bitset = 1 << v
            self.intset = {v}
        elif isinstance(v, str):
            bit = EXTENDED_ITEM[v]
            self.bitset = 1 << bit
            self.intset = {bit}
        elif isinstance(v, tuple):  # Item, count
            item, count = v
            assert count <= ITEM_COUNTS[item]
            if ITEM_COUNTS[item] == 1:
                bit = EXTENDED_ITEM[item]
                self.bitset = 1 << bit
                self.intset = {bit}
            else:
                self.bitset = 0
                self.intset = set()
                for i in range(count):
                    bit = EXTENDED_ITEM[f"{item} #{i}"]
                    self.bitset |= 1 << bit
                    self.intset.add(bit)

    def __getitem__(self, index):
        if isinstance(index, EXTENDED_ITEM):
            return bool(self.bitset & (1 << index))
        else:
            raise ValueError

    def __or__(self, other):
        if isinstance(other, EXTENDED_ITEM):
            return Inventory(self.bitset | (1 << other), self.intset | {other})
        elif isinstance(other, Inventory):
            return Inventory(self.bitset | other.bitset, self.intset | other.intset)
        else:
            raise ValueError

    def __and__(self, other):
        if isinstance(other, Inventory):
            return Inventory(self.bitset & other.bitset, self.intset & other.intset)
        else:
            raise ValueError

    def __le__(self, other):
        """Define inclusion"""
        return self.bitset | other.bitset == other.bitset

    @staticmethod
    def add(self, item):
        if isinstance(item, EXTENDED_ITEM) or isinstance(item, Inventory):
            return self | item
        elif isinstance(item, str):
            if ITEM_COUNTS[item] == 1 and not self[(item_bit := EXTENDED_ITEM[item])]:
                return self | item_bit
            else:
                for i in range(ITEM_COUNTS[item]):
                    if not self[(item_bit := EXTENDED_ITEM[f"{item} #{i}"])]:
                        return self | item_bit
        raise ValueError

    @staticmethod
    def remove(self, item):
        if isinstance(item, EXTENDED_ITEM):
            return Inventory(self.bitset & ~(1 << item), self.intset.difference({item}))
        elif isinstance(item, str):
            for i in reversed(range(ITEM_COUNTS[item])):
                if self[(item_bit := EXTENDED_ITEM[f"{item} #{i}"])]:
                    return Inventory(
                        self.bitset & ~(1 << item_bit),
                        self.intset.difference({item_bit}),
                    )
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
