from typing import (
    List,
    NewType,
    DefaultDict,
    Dict,
    Callable,
    Any,
    Iterable,
    Tuple,
    Optional,
    Set,
)
from dataclasses import dataclass
from functools import reduce
from enum import IntEnum
from collections import OrderedDict, defaultdict
from abc import ABC
import re
from itertools import product

from .item_types import ALL_ITEM_NAMES, INVENTORY_ITEMS
from .inventory import Inventory, RevInventory

from options import Options, OPTIONS

Macros = "Dict[str, LogicExpression]"

# LocationName = NewType("LocationName", str)
ItemName = NewType("ItemName", str)


class LogicExpression(ABC):
    def localize(
        self, localizer: Callable[str, Optional[Tuple[List[str], str]]]
    ) -> "LogicExpression":
        raise NotImplementedError

    def specialize(self, options: Options) -> "LogicExpression":
        raise NotImplementedError

    def eval(self, inventory: Inventory, world: "World") -> bool:
        raise NotImplementedError

    def get_items_needed(
        self,
    ) -> Set[Inventory]:
        raise NotImplementedError

    # def __str__(self):
    #     raise NotImplementedError("abstract")


@dataclass
class DNFInventory(LogicExpression):
    disjunction: Set[Inventory]

    def eval(self, inventory: Inventory):
        return any(req_items | inventory == inventory for req_items in self.disjunction)

    def specialize(self, *args):
        return self

    def localize(self, *args):
        return self


def ConstantAtom(value: bool) -> LogicExpression:
    if value:
        return DNFInventory(set(Inventory()))
    else:
        return DNFInventory(set())


@dataclass
class OptionAtom(LogicExpression):
    option_name: str
    predicate: Callable[[Any], bool]

    def eval(self, *args):
        raise TypeError(
            "f{self.__class__.__name__} must be specialized to be evaluated"
        )

    def specialize(self, options: Options):
        return ConstantAtom(self.predicate(options[self.option_name]))

    def localize(self, *args):
        return self


@dataclass
class TrickAtom(LogicExpression):
    trick_name: str

    def eval(self, *args):
        raise TypeError(
            "f{self.__class__.__name__} must be specialized to be evaluated"
        )

    def specialize(self, options: Options):
        return ConstantAtom(self.trick_name in options.get("enabled-tricks", []))

    def localize(self, *args):
        return self


def InventoryAtom(item_name: str, quantity: int) -> LogicExpression:
    return DNFInventory(Inventory((item_name, quantity)))


def EventAtom(event_address: List[str], event_name: str) -> LogicExpression:
    name = "/".join(event_address) + "/" + event_name
    return DNFInventory(Inventory((name, 1)))


@dataclass
class BasicTextAtom(LogicExpression):
    text: str

    def eval(self, *args):
        raise TypeError("Text must be localized to be evaluated")

    def specialize(self, *args):
        return self

    def localize(self, localizer):
        if (v := localizer(self.text)) is None:
            raise ValueError(f"Unknown event {self.text}")
        else:
            return EventAtom(*v)


@dataclass
class AndCombination(LogicExpression):
    arguments: List[LogicExpression]

    @staticmethod
    def simplify(arguments: Iterable[LogicExpression]) -> LogicExpression:
        if all(map(lambda x: isinstance(x, DNFInventory), arguments)):
            disjunctions = map(lambda x: x.disjunction, arguments)
            bigset = set()
            for conjunction_tuple in product(*disjunctions):
                bigset.add(reduce(Inventory.__and__, conjunction_tuple, RevInventory()))
            return DNFInventory(Inventory.simplify_invset(bigset))
        else:
            return AndCombination(arguments)

    def specialize(self, options: Options):
        self.simplify(arg.specialize(options) for arg in self.arguments)

    def localize(self, localizer):
        self.simplify(arg.localize(localizer) for arg in self.arguments)

    def eval(self, *args):
        raise TypeError(
            f"Some argument of this {type(self).__name__} cannot be evaluated, or something has gone wrong"
        )


@dataclass
class OrCombination(LogicExpression):
    arguments: List[LogicExpression]

    @staticmethod
    def simplify(arguments: Iterable[LogicExpression]) -> LogicExpression:
        if all(map(lambda x: isinstance(x, DNFInventory), arguments)):
            bigset = reduce(set.union, map(lambda x: x.disjunction, arguments), set())
            return DNFInventory(Inventory.simplify_invset(bigset))
        else:
            return OrCombination(arguments)

    def specialize(self, options: Options):
        self.simplify(arg.specialize(options) for arg in self.arguments)

    def localize(self, localizer):
        self.simplify(arg.localize(localizer) for arg in self.arguments)

    def eval(self, *args):
        raise TypeError(
            f"Some argument of this {type(self).__name__} cannot be evaluated, or something has gone wrong"
        )


# Parsing

option_re = re.compile(r"^Option .*$")
positive_boolean_re = re.compile(r"^Option \"([^\"]+)\" Enabled$")
negative_boolean_re = re.compile(r"^Option \"([^\"]+)\" Disabled$")
positive_dropdown_re = re.compile(r"^Option \"([^\"]+)\" Is \"([^\"]+)\"$")
negative_dropdown_re = re.compile(r"^Option \"([^\"]+)\" Is Not \"([^\"]+)\"$")
positive_list_re = re.compile(r"^Option \"([^\"]+)\" Contains \"([^\"]+)\"$")
negative_list_re = re.compile(r"^Option \"([^\"]+)\" Does Not Contain \"([^\"]+)\"$")

trick_re = re.compile(r"^Trick (.*)$")
item_with_count_re = re.compile(r"^(.+) ×[ ]*(\d+)$")


from lark import Lark, Transformer, v_args

exp_grammar = """
    ?start: disjunction

    ?disjunction: conjunction
        | disjunction "|" conjunction -> mk_or

    ?conjunction: atom
        | conjunction "&" atom -> mk_and

    ?atom: TEXT -> mk_atom
         | "(" disjunction ")"

    TEXT: /[^|&())]+/

    %import common.WS
    %ignore WS
"""


@v_args(inline=True)  # Affects the signatures of the methods
class MakeExpression(Transformer):
    def mk_or(self, left, right):
        if isinstance(left, OrCombination):
            return OrCombination(left.arguments + [right])
        else:
            return OrCombination([left, right])

    def mk_and(self, left, right):
        if isinstance(left, AndCombination):
            return AndCombination(left.arguments + [right])
        else:
            return AndCombination([left, right])

    def mk_atom(self, text):
        text = text.strip()

        # Test for option
        if option_re.search(text):
            if match := positive_boolean_re.search(text):
                option_name = match.group(1)
                predicate = lambda b: bool(b)
            elif match := negative_boolean_re.search(text):
                option_name = match.group(1)
                predicate = lambda b: not b
            elif match := positive_dropdown_re.search(text):
                option_name = match.group(1)
                value = match.group(2)
                predicate = lambda v, value=value: v == value
            elif match := negative_dropdown_re.search(text):
                option_name = match.group(1)
                value = match.group(2)
                predicate = lambda v, value=value: v != value
            elif match := positive_list_re.search(text):
                option_name = match.group(1)
                value = match.group(2)
                predicate = (
                    lambda lst, value=value: value in lst if lst is not None else False
                )
            elif match := negative_list_re.search(text):
                option_name = match.group(1)
                value = match.group(2)
                predicate = (
                    lambda lst, value=value: value not in lst
                    if lst is not None
                    else True
                )
            else:
                raise ValueError(f"Option pattern not recognized: {text}")

            if option_name not in OPTIONS:
                raise ValueError(f"Unknown option {option_name}")
            return OptionAtom(option_name, predicate)

        elif match := trick_re.search(text):
            # Check validity of trick name
            return TrickAtom(match.group(1))

        elif match := item_with_count_re.search(text):
            item_name = match.group(1)
            if item_name not in ALL_ITEM_NAMES:
                raise ValueError(f"Unknown item {item_name}")
            return InventoryAtom(item_name, int(match.group(2)))

        elif text in ALL_ITEM_NAMES:
            return InventoryAtom(text, 1)

        else:
            return BasicTextAtom(text)


exp_parser = Lark(exp_grammar, parser="lalr", transformer=MakeExpression())
LogicExpression.parse = exp_parser.parse


# def check_option_enabled_requirement(options: Options, exp: str) -> bool:
#     exp = LogicExpression.parse(exp)
#     exp = exp.specialize(options)
#     return exp.eval(Inventory())


# def test():
#     import yaml

#     with open("SS Rando Logic - Requirements.yaml") as f:
#         locations = yaml.safe_load(f)
#     for loc in locations:
#         req_str = locations[loc]
#         print(f"{loc}: {req_str}")
#         print(f"-> {LogicExpression.parse(req_str)}")
#         print()
