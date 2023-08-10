import argparse
from argparse import Namespace
from enum import Enum

from src.img_to_text_converter import GreyscaleVariants

APP_DESCRIPTION = "Malý nástroj na přehrávání vtipných momentů z Griffinových, " \
                  "Subway Surfers a jiných zábavných videí v konzoli"


def initialize_parser() -> Namespace:
    parser = argparse.ArgumentParser(
        description=APP_DESCRIPTION,
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=27)
    )
    __initialize_type_arg(parser)
    __initialize_grey_scale_arg(parser)
    __initialize_repeat_arg(parser)
    args = parser.parse_args()
    return args


def __initialize_type_arg(parser: argparse.ArgumentParser) -> None:
    args_list = list(TypeArg)
    default_type = TypeArg.SUBWAY_SURFERS
    help_text = f"Druh videa pro přehrání\n" \
                f"{__format_choices(args_list)}" \
                f"\nVýchozí hodnota: {default_type}"
    parser.add_argument(
        "-t",
        "--type",
        type=TypeArg,
        help=help_text,
        metavar='',
        choices=args_list,
        default=default_type
    )


def __initialize_grey_scale_arg(parser: argparse.ArgumentParser) -> None:
    greyscale_variants = list(GreyscaleVariants)
    default_greyscale_variant = GreyscaleVariants.DEPTH_10_REVERSED.name.lower()
    help_text = f"Druh ascii reprezentace videa\n" \
                f"{__format_choices(greyscale_variants)}\n" \
                f"Výchozí hodnota: {default_greyscale_variant}"
    parser.add_argument(
        "-g",
        "--greyscale-chars",
        type=lambda name: GreyscaleVariants[name.upper()],
        help=help_text,
        metavar='',
        choices=greyscale_variants,
        default=default_greyscale_variant
    )


def __initialize_repeat_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--repeat",
        help="Přehrávat ve smyčce",
        action=argparse.BooleanOptionalAction,
        default=False
    )


def __format_choices(choices: list[any]) -> str:
    return f"Možnosti: ({', '.join([str(item) for item in choices])})"


class TypeArg(Enum):
    SUBWAY_SURFERS = "subway-surfers"
    FAMILY_GUY = "family-guy"

    def __str__(self):
        return self.value
