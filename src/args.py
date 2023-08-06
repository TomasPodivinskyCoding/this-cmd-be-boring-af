import argparse
from argparse import Namespace
from enum import Enum

# description = "A little tool to show subway surfers, family guy funny moments and other entertaining clips in console"
description = "Malý nástroj na přehrávání vtipných momentů z Griffinových, Subway Surfers a jiných zábavných videí v konzoli"


def initialize_parser() -> Namespace:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-t", "--type", help="Druh videa pro přehrání", type=TypeArg, choices=list(TypeArg),
                        default=TypeArg.subway)
    parser.add_argument("-r", "--repeat", help="Přehrávat ve smyčce", action=argparse.BooleanOptionalAction,
                        default=False)
    args = parser.parse_args()
    return args


class TypeArg(Enum):
    subway = "subway"
    family = "family-guy"

    def __str__(self):
        return self.value
