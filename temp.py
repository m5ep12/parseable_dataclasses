from argparse import ArgumentParser, Action, BooleanOptionalAction
from dataclasses import dataclass, fields
from pprint import pprint
from typing import Any, Literal, Sequence, get_args, get_origin

t1 = list[int]
t2 = int | str

pprint([get_origin(t) for t in [t1, t2]])

@dataclass
class DC:
    a: int
    b: list

class PrintAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print("[{}] option add value [{}] as attr [{}]".format(
                option_string, values, self.dest))
        setattr(namespace, self.dest, values)


def printing_tuple(arg):
    print(arg)
    return arg

# p = ArgumentParser()
# p.add_argument("--r", nargs=3, action=PrintAction)
# args = p.parse_args("--r a b c".split())
# pprint(args)

#p = ArgumentParser()
#p.add_argument("a", type=int, default=None)
#p.add_argument("--b", type=float, nargs="*")
#args = p.parse_args("--b -- 10".split())
#dc = DC(**vars(args))


p = ArgumentParser()
l = Literal[1.0, 2.0, 3.0]
args = get_args(l)
types = set(map(type, args))
print(types)
t = types.pop()
print(t.__name__)
p.add_argument("a", type=t, choices=args, help=t.__name__)
p.add_argument("--op", action=BooleanOptionalAction)
args = p.parse_args("3.0 --no-op --help".split())
pprint(args)

