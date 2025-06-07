"""parseable-dataclasses
"""
from abc import ABC
from dataclasses import MISSING, dataclass, fields, Field, is_dataclass
from argparse import Action, ArgumentParser, BooleanOptionalAction, Namespace, _StoreTrueAction
from typing import Any, Literal, Sequence, get_args, get_origin, override

# I referenced https://github.com/lidatong/dataclasses-json

class ParsearbleDataClassMixin(ABC):

    @classmethod
    def parse_args(cls, args: Sequence[str] | None = None):
        parser = cls.ArgumentParser()
        namespace = parser.parse_args(args=args)
        return cls(**vars(namespace))

    @classmethod
    def ArgumentParser(cls) -> ArgumentParser:
        assert is_dataclass(cls), f"This mixin must be inherited to a dataclass, but {cls=} is not in dataclasses."
        parser = ArgumentParser(cls.__name__)
        for field in fields(cls):
            name = field.name if is_positional(field) else "--" + field.name
            default = field.name if is_positional(field) else "--" + field.name
            if is_positional(field):
                name = field.name
                default = None
            else:
                name = "--" + field.name
                if field.default is not MISSING:
                    default = field.default
                else:
                    assert callable(field.default_factory), f"default_factory must be callable, but {field.default_factory=} is not callable!"
                    default = field.default_factory()

            match field.type:
                case t if t in (int, float, str):
                    # p: T
                    t: type
                    text = t.__name__
                    parser.add_argument(name, default=default, type=t, help=text)
                case t if t == bool:
                    # p: bool
                    text = f"default is {default if default else False}"
                    parser.add_argument(name, default=default, action=BooleanOptionalAction, help=text)
                case t if t == list:
                    # p: list
                    text = "list[str]"
                    parser.add_argument(name, default=default, nargs="*", type=str)
                case t if get_origin(t) == list:
                    # p: list[T]
                    arg: type = get_args(t)[0]
                    text = f"list[{arg.__name__}]"
                    parser.add_argument(name, default=default, nargs="*", type=arg)
                case t if get_origin(t) == Literal:
                    # p: Literal[...]
                    args = get_args(t)
                    types = set(map(type, args))
                    assert len(types) == 1, "all the types of a literal field must be the same, but there are multiple types in this literal field as {types=}."
                    typeofliteral = types.pop()
                    text = typeofliteral.__name__
                    parser.add_argument(name, default=default, choices=args, type=typeofliteral)
                case _:
                    raise ValueError
        return parser


def is_positional(field: Field) -> bool:
    """return True if input is a positional field

    Args:
        field (Field):

    Returns:
        bool: True/False
    """
    return field.default is MISSING and field.default_factory is MISSING

def is_optional(field: Field) -> bool:
    """return True if input is a optional field

    Args:
        field (Field):

    Returns:
        bool: True/False
    """
    return not is_positional(field)