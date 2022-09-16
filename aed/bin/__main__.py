#! /user/bin/env python3

import argparse
from aed.tui.alacritty_tui import Tui
from aed.container.alacritty_container import (
    AlacrittyContainer,
    ALACRITTY_CONFIG,
    ALACRITTY_COLOR_DIR,
    ALACRITTY_FONT_DIR,
    yaml,
)


def parse_input():
    parser = argparse.ArgumentParser(
        description="CLI and TUI tool for quickly editing Alacritty color/font/opacity options. The TUI will be launced if no options are specified."
    )
    parser.add_argument(
        "--colors",
        type=str,
        help="path to valid YAML file defining desired Alacritty color options",
    )
    parser.add_argument(
        "--font",
        type=str,
        help="path to valid YAML file defining desired Alacritty font options",
    )
    parser.add_argument(
        "--opacity",
        type=float,
        help="number from 0.0 to 1.0 inclusive to define a new window opacity. All valid input is rounded to the nearest hundredth.",
    )
    return parser


def main():
    parser = parse_input()
    opts = parser.parse_args()

    ac = AlacrittyContainer(ALACRITTY_CONFIG, ALACRITTY_COLOR_DIR, ALACRITTY_FONT_DIR)
    if opts.colors:
        with open(opts.colors, "r") as cfile:
            color_map = yaml.load(cfile)
        exception = ac._validate_colors(color_map)
        if exception != None:
            raise exception
        else:
            ac.alacritty_config["colors"] = color_map["colors"]
            ac.dump_current_alacritty_config()

    if opts.font:
        with open(opts.font, "r") as ffile:
            font_map = yaml.load(ffile)
        exception = ac._validate_fonts(font_map)
        if exception != None:
            raise exception
        else:
            ac.alacritty_config["font"] = font_map["font"]
            ac.dump_current_alacritty_config()

    if opts.opacity != None:
        opacity = round(opts.opacity, 2)
        exception = ac.set_opacity(opacity)
        if exception != None:
            raise exception

    if len([opt for opt, val in vars(opts).items() if val != None]) == 0:
        tui = Tui(ac)


if __name__ == "__main_":
    main()
