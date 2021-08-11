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
)
from dataclasses import dataclass
from functools import reduce
from collections import OrderedDict, defaultdict
from abc import ABC
import re

from .item_types import ALL_ITEM_NAMES

from options import Options, OPTIONS

Macros = "Dict[str, LogicExpression]"

# LocationName = NewType("LocationName", str)
# ItemName = NewType("ItemName", str)


class Inventory(DefaultDict[str, int]):
    def __init__(self):
        super().__init__(int)

    def add(self, item):
        self[item] += 1

    def remove(self, item):
        if self[item] > 0:
            self[item] -= 1

    def all_owned_unique_items(self):
        return set((item for item, count in self.items() if count >= 1))


class LogicExpression(ABC):
    def localize(
        self, localizer: Callable[str, Optional[Tuple[List[str], str]]]
    ) -> "LogicExpression":
        raise NotImplementedError

    def inline(self, macros: Macros) -> "LogicExpression":
        raise NotImplementedError

    def specialize(self, options: Options) -> "LogicExpression":
        raise NotImplementedError

    def eval(self, inventory: Inventory, world: "World") -> bool:
        raise NotImplementedError

    # def get_items_needed(
    #     self, options: Options, inventory: Inventory, macros
    # ) -> OrderedDict:  # itemname -> count
    #     raise NotImplementedError("abstract")

    # def __str__(self):
    #     raise NotImplementedError("abstract")


@dataclass
class ConstantAtom(LogicExpression):
    value: bool

    def eval(self, *args):
        return self.value

    def specialize(self, *args):
        return self

    def inline(self, *args):
        return self

    def localize(self, *args):
        return self

    # def get_items_needed(
    #     self, options: Options, inventory: Inventory, macros
    # ) -> OrderedDict:  # itemname, count
    #     if self.value:
    #         return OrderedDict()
    #     else:
    #         return


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

    def inline(self, *args):
        return self

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

    def inline(self, *args):
        return self

    def localize(self, *args):
        return self


@dataclass
class InventoryAtom(LogicExpression):
    item_name: str
    quantity: int

    def eval(self, inventory: Inventory, world):
        return inventory[self.item_name] >= self.quantity

    def specialize(self, *args):
        return self

    def inline(self, *args):
        return self

    def localize(self, *args):
        return self

    # def get_items_needed(
    #     self, options: Options, inventory: Inventory, macros
    # ) -> OrderedDict:  # itemname, count
    #     return OrderedDict({self.item_name: self.quantity})


@dataclass
class EventAtom(LogicExpression):
    event_address: List[str]
    event_name: str

    def eval(self, inventory: Inventory, world: "World"):
        return world.is_event_accessible(self.event_address, self.event_name, inventory)

    def specialize(self, *args):
        return self

    def inline(self, *args):
        return self

    def localize(self, *args):
        return self


@dataclass
class MacroAtom(LogicExpression):
    macro_name: str

    def eval(self, *args):
        raise TypeError("Macros must be inlined to be evaluated")

    def specialize(self, *args):
        return self

    def inline(self, macros: Macros):
        res = macros[self.macro_name]
        if res is None:
            raise ValueError(f"Unknown {self.macro_name} macro")
        return res

    def localize(self, *args):
        return self


@dataclass
class BasicTextAtom(LogicExpression):
    text: str

    def eval(self, *args):
        raise TypeError("Text must be localized to be evaluated")

    def specialize(self, *args):
        return self

    def inline(self, *args):
        raise TypeError("Text must be localized to inline macros")

    def localize(self, localizer):
        v = localizer(self.text)
        if v is None:
            return MacroAtom(self.text)
        else:
            return EventAtom(*v)


@dataclass
class AndCombination(LogicExpression):
    arguments: List[LogicExpression]

    @staticmethod
    def extract_and(arg: LogicExpression) -> List[LogicExpression]:
        if isinstance(arg, AndCombination):
            return arg.arguments
        elif arg == ConstantAtom(True):
            return []
        else:
            return [arg]

    @staticmethod
    def simplify(arguments: Iterable[LogicExpression]) -> LogicExpression:
        if ConstantAtom(False) in arguments:
            return ConstantAtom(False)
        conjunction_lists = map(AndCombination.extract_and, arguments)
        flattened = reduce(list.append, conjunction_lists)
        if len(flattened):
            return AndCombination(flattened)
        else:
            return ConstantAtom(True)

    def inline(self, macros: Macros):
        self.simplify(arg.inline(macros) for arg in self.arguments)

    def specialize(self, options: Options):
        self.simplify(arg.specialize(options) for arg in self.arguments)

    def localize(self, localizer):
        self.simplify(arg.localize(localizer) for arg in self.arguments)

    def eval(self, inventory: Inventory):
        return all(arg.eval(inventory) for arg in self.arguments)

    # def get_items_needed(
    #     self, options: Options, inventory: Inventory, macros
    # ) -> OrderedDict:  # itemname, count
    #     items_needed = OrderedDict()

    #     if not len(self.arguments):  # Bad practice, this should have been simplified
    #         return None
    #     for subresult in (
    #         arg.get_items_needed(options, inventory, macros) for arg in self.arg
    #     ):
    #         if subresult is None:  # if one is unreachable, all of this is
    #             return None

    #         for item_name, num_required in subresult.items():
    #             items_needed[item_name] = max(
    #                 num_required, items_needed.setdefault(item_name, 0)
    #             )

    #     return items_needed


@dataclass
class OrCombination(LogicExpression):
    arguments: List[LogicExpression]

    @staticmethod
    def extract_or(arg):
        if isinstance(arg, OrCombination):
            return arg.arguments
        elif arg == ConstantAtom(False):
            return []
        else:
            [arg]

    @staticmethod
    def simplify(arguments: Iterable[LogicExpression]) -> LogicExpression:
        if ConstantAtom(True) in arguments:
            return ConstantAtom(True)
        conjunction_lists = map(OrCombination.extract_or, arguments)
        flattened = reduce(list.append, conjunction_lists)
        if len(flattened):
            return OrCombination(flattened)
        else:
            return ConstantAtom(False)

    def inline(self, macros: Macros):
        self.simplify(arg.inline(macros) for arg in self.arguments)

    def specialize(self, options: Options):
        self.simplify(arg.specialize(options) for arg in self.arguments)

    def localize(self, localizer):
        self.simplify(arg.localize(localizer) for arg in self.arguments)

    def eval(self, inventory: Inventory):
        return any(arg.eval(inventory) for arg in self.arguments)

    # def get_items_needed(
    #     self, options: Options, inventory: Inventory, macros
    # ) -> OrderedDict:  # itemname, count
    #     items_needed = OrderedDict()
    #     raise NotImplementedError


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
        print(text)
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
            return MacroAtom(text)


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
