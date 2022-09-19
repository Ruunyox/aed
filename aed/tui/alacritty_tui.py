import urwid
import os
from typing import Union, List, Callable
from aed.container.alacritty_container import AlacrittyContainer


class Tui(object):
    """Urwid text user interface for manipulating Alacritty color, font, and opacity options

    Parameters
    ----------
    container:
        An instance of `AlacrittyContainer` which encompasses the Alacritty configuration
        to be edited, as well as the available font and color options.
    """

    _palette = [
        ("menu", "white", "black"),
        ("reversed", "standout", ""),
        ("_black", "white", "black"),
        ("_red", "white", "dark red"),
        ("_green", "white", "dark green"),
        ("_yellow", "white", "brown"),
        ("_blue", "white", "dark blue"),
        ("_magenta", "white", "dark magenta"),
        ("_cyan", "white", "dark cyan"),
        ("_white", "white", "light gray"),
        ("_bblack", "white", "dark gray"),
        ("_bred", "white", "light red"),
        ("_bgreen", "white", "light green"),
        ("_byellow", "white", "yellow"),
        ("_bblue", "white", "light blue"),
        ("_bmagenta", "white", "light magenta"),
        ("_bcyan", "white", "light cyan"),
        ("_bwhite", "white", "white"),
        ("header", "black", "dark green"),
        ("filled", "white", "black"),
        ("unfilled", "black", "white"),
        ("red_", "dark red", "black"),
        ("green_", "dark green", "black"),
        ("yellow_", "brown", "black"),
        ("blue_", "dark blue", "black"),
        ("magenta_", "dark magenta", "black"),
    ]

    _color_keys = [
        "_black",
        "_red",
        "_green",
        "_yellow",
        "_blue",
        "_magenta",
        "_cyan",
        "_white",
    ]
    _bright_color_keys = [
        "_bblack",
        "_bred",
        "_bgreen",
        "_byellow",
        "_bblue",
        "_bmagenta",
        "_bcyan",
        "_bwhite",
    ]

    _menu_style_kwargs = {
        "tline": "\N{BOX DRAWINGS DOUBLE HORIZONTAL}",
        "trcorner": "\N{BOX DRAWINGS DOWN SINGLE AND LEFT DOUBLE}",
        "tlcorner": "\N{BOX DRAWINGS DOWN SINGLE AND RIGHT DOUBLE}",
    }

    def __init__(self, container: AlacrittyContainer):
        self.container = container

        if "opacity" not in list(self.container.alacritty_config["window"].keys()):
            base_opacity = 1.0
        else:
            base_opacity = self.container.alacritty_config["window"]["opacity"]

        menu1 = Tui._make_select_menu(
            list(self.container.colors.keys()),
            self.container.set_named_colors,
            "[ COLORS ]",
        )
        menu2 = Tui._make_select_menu(
            list(self.container.fonts.keys()),
            self.container.set_named_font,
            "[ FONTS ]",
        )
        menu3 = Tui._make_opacity_box(base_opacity)
        menu4 = Tui._make_font_display()
        menu5 = Tui._make_color_display()

        color_display = Tui._make_color_display()
        self.top = Tui._make_top(menu1, menu2, menu3, menu4, menu5)
        self.loop = urwid.MainLoop(
            self.top,
            palette=Tui._palette,
            unhandled_input=self._handle_input,
            handle_mouse=False,
        )
        self.loop.run()

    def _urwid_quit(*args):
        """Deconstructs the TUI and quits the program"""
        raise urwid.ExitMainLoop()

    def _handle_input(self, key: str):
        """Handles general keyboard input during the TUI loop"""
        if key in ("Q", "q"):
            self._urwid_quit()
        if key in ("-"):
            new_opacity = self.container.alacritty_config["window"]["opacity"] - 0.01
            if self.container.set_opacity(new_opacity) == None:
                self.update_opacity_bar(new_opacity)
        if key in ("+"):
            new_opacity = self.container.alacritty_config["window"]["opacity"] + 0.01
            if self.container.set_opacity(new_opacity) == None:
                self.update_opacity_bar(new_opacity)

    @staticmethod
    def _make_top(
        menu1: urwid.AttrMap,
        menu2: urwid.AttrMap,
        menu3: urwid.AttrMap,
        menu4: urwid.AttrMap,
        menu5: urwid.AttrMap,
    ) -> urwid.Frame:
        """combines menu widgets into an urwid.Frame-wrapped urwid.Overlay

               +----------------------+-------------------+
               |                      |                   |
               |     menu1            |     menu2         |
               |                      |                   |
               |                      |                   |
               +----------------------+-------------------+
               |                  menu3                   |
               +------------------------------------------+
               |                                          |
               |                  menu4                   |
               |                                          |
               +------------------------------------------+
               |                                          |
               |                  menu5                   |
               |                                          |
               +------------------------------------------+

        Parameters
        ----------
        menu1:
            first menu
        menu2:
            second menu
        menu3:
            third menu
        menu4:
            fourth menu
        menu5:
            fifth menu

        Returns
        -------
        top:
            urwid.Frame(urwid.Overlay) containing the grouped windows
        """

        top = urwid.Overlay(
            urwid.Pile(
                [urwid.Columns([menu1, menu2]), (3, menu3), (7, menu4), (4, menu5)]
            ),
            urwid.SolidFill(" "),
            align="center",
            width=("relative", 90),
            valign="middle",
            height=("relative", 90),
        )
        top = urwid.Frame(
            top,
            header=urwid.AttrMap(
                urwid.Text("ALACRITTY EDITOR", align="center"), "header"
            ),
        )
        return top

    @staticmethod
    def _make_font_display() -> urwid.AttrMap:
        """Generates a font sample to assess font character distinguishability"""

        attrs = ["red_", "green_", "yellow_", "blue_", "magenta_"]
        lines = [
            "o0O s5S z2Z !|l1Iij {([|])}.,;:``''\"\" uvwvu",
            "a@#* vVuUwW <>;^=           -~\/\/ -- == __",
            "the quick brown fox jumps over the lazy dog",
            "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
            "0123456789 &-+@ for (int i=0; i<=j; ++i) {}",
        ]
        text = urwid.Pile(
            [
                urwid.Filler(urwid.AttrMap(urwid.Text(line, align="center"), attr))
                for line, attr in zip(lines, attrs)
            ]
        )
        font_display = urwid.AttrMap(
            urwid.LineBox(text, **Tui._menu_style_kwargs),
            "menu",
        )
        return font_display

    @staticmethod
    def _make_color_display() -> urwid.AttrMap:
        """Generates a display of the current normal/bright shell colors 0-15"""

        colors = [
            urwid.Filler(urwid.AttrMap(urwid.Text(" "), attr))
            for attr in Tui._color_keys
        ]
        bright_colors = [
            urwid.Filler(urwid.AttrMap(urwid.Text(" "), attr))
            for attr in Tui._bright_color_keys
        ]
        color_display = urwid.AttrMap(
            urwid.LineBox(
                urwid.Pile([urwid.Columns(colors), urwid.Columns(bright_colors)]),
                **Tui._menu_style_kwargs
            ),
            "menu",
        )
        return color_display

    @staticmethod
    def _make_opacity_box(opacity: float) -> urwid.AttrMap:
        """Generates a linear gauge of the current shell window opacity"""
        percent = opacity * 100.0
        bar = urwid.ProgressBar("filled", "unfilled", percent)
        opacity_box = urwid.AttrMap(
            urwid.LineBox(
                urwid.Filler(bar), title="[ Opacity ]", **Tui._menu_style_kwargs
            ),
            "menu",
        )
        return opacity_box

    @staticmethod
    def _make_select_menu(
        choices: List[str], action: Callable, title="Title"
    ) -> urwid.AttrMap:
        """Generates a simple list of buttons that are signal connected to a supplied action

        Parameters
        ----------
        choices:
            List of strings, one for each button. These strings are passed as arguments to the
            supplied action.
        action:
            Funcion/method to which the `click` signal of each button will be connected
        title:
            Title of the urwid.LineBox that wraps the button list

        Returns
        -------
        menu:
            urwid.AttrMap(urwid.Linebox) that contains the list of buttons, one for each choice
        """

        buttons = []
        for c in choices:
            button = urwid.Button(c)
            urwid.connect_signal(button, "click", action, user_args=[c])
            buttons.append(button)
        body = [urwid.AttrMap(button, None, focus_map="reversed") for button in buttons]
        walker = urwid.SimpleFocusListWalker(body)
        menu = urwid.LineBox(
            urwid.ListBox(walker), title=title, **Tui._menu_style_kwargs
        )
        menu = urwid.AttrMap(menu, "menu")
        return menu

    def update_opacity_bar(self, opacity: float):
        """Updates the opacity gauge to the input opacity"""
        percent = opacity * 100.0
        self.top.body.top_w.contents[1][0].base_widget.set_completion(percent)
