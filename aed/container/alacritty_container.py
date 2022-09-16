import os
from ruamel.yaml import YAML
from glob import glob
from typing import Union, List, Callable

HOME = os.path.expanduser("~")
ALACRITTY_CONFIG = os.path.join(HOME, ".config/alacritty/alacritty.yml")
ALACRITTY_COLOR_DIR = os.path.join(HOME, ".config/alacritty/colors")
ALACRITTY_FONT_DIR = os.path.join(HOME, ".config/alacritty/fonts")

yaml = YAML(typ="safe")
yaml.default_flow_style = False


class AlacrittyContainer(object):
    """Class for loading, modifying and dumping an Alacritty configuration file

    Parameters
    ----------
    config_fn:
        String specifying the abosolute path to the Alacritty configuraion YAML file
    color_dir:
        String specifying the absolute path to a directory containing YAML (.yml)
        files specifying standard Alacritty color options. E.g., :

            colors:
              primary:
                background: '#1d1f21'
                foreground: '#c5c8c6'
                dim_foreground: '#828482'
                bright_foreground: '#eaeaea'
              cursor:
                text: CellBackground
                cursor: CellForeground
              vi_mode_cursor:
                text: CellBackground
                cursor: CellForeground
              search:
                matches:
                  foreground: '#000000'
                  background: '#ffffff'
                focused_match:
                  foreground: '#ffffff'
                  background: '#000000'
              hints:
                start:
                  foreground: '#1d1f21'
                  background: '#e9ff5e'
                end:
                  foreground: '#e9ff5e'
                  background: '#1d1f21'
              line_indicator:
                foreground: None
                background: None
              footer_bar:
                background: '#c5c8c6'
                foreground: '#1d1f21'
              selection:
                text: CellBackground
                background: CellForeground
              normal:
                black:   '#1d1f21'
                red:     '#cc6666'
                green:   '#b5bd68'
                yellow:  '#f0c674'
                blue:    '#81a2be'
                magenta: '#b294bb'
                cyan:    '#8abeb7'
                white:   '#c5c8c6'
              bright:
                black:   '#666666'
                red:     '#d54e53'
                green:   '#b9ca4a'
                yellow:  '#e7c547'
                blue:    '#7aa6da'
                magenta: '#c397d8'
                cyan:    '#70c0b1'
                white:   '#eaeaea'
              dim:
                black:   '#131415'
                red:     '#864343'
                green:   '#777c44'
                yellow:  '#9e824c'
                blue:    '#556a7d'
                magenta: '#75617b'
                cyan:    '#5b7d78'
                white:   '#828482'
              indexed_colors: []
              transparent_background_colors: false

    font_dir:
        String specifying the absolute path to a directory containing YAML (.yml)
        files specifying standard Alacritty font options. E.g., :

            font:
              normal:
                family: monospace
                style: Regular
              bold:
                family: monospace
                style: Bold
              italic:
                family: monospace
                style: Italic
              bold_italic:
                family: monospace
                style: Bold Italic
              size: 11.0
              offset:
                x: 0
                y: 0
              glyph_offset:
                x: 0
                y: 0
              builtin_box_drawing: true
            draw_bold_text_with_bright_colors: false
    """

    _color_options = set(
        [
            "primary",
            "normal",
            "bright",
            "cursor",
            "vi_mode_cursor",
            "search",
            "hints",
            "line_indicator",
            "footer_bar",
            "selection",
            "dim",
            "indexed_colors",
            "transparent_background_colors",
        ]
    )
    _font_options = set(
        [
            "normal",
            "bold",
            "italic",
            "bold_italic",
            "size",
            "offset",
            "glyph_offset",
            "use_thin_strokes",
            "builtin_box_drawing",
        ]
    )

    def __init__(
        self,
        config_fn: str,
        color_dir: str = ALACRITTY_COLOR_DIR,
        font_dir: str = ALACRITTY_FONT_DIR,
    ):
        self.config_fn = config_fn
        self.alacritty_config = AlacrittyContainer.load_yaml(self.config_fn)
        self.colors = AlacrittyContainer.get_colors(color_dir)
        self.fonts = AlacrittyContainer.get_fonts(font_dir)

    @staticmethod
    def get_colors(color_dir: str) -> dict[str, str]:
        """Grabs all color YAML filenames from the supplied `color_dir`

        Parameters
        ----------
        color_dir:
            String of the absolute path to the directory where alacritty
            color options are stored as YAML files

        Returns
        -------
        colors:
            Dictionary where the color file basenames are keys and the associated
            absolute file paths are the values
        """

        color_files = sorted(glob("{}/*.yml".format(color_dir)))
        colors = {}
        for fn in color_files:
            name = fn.split("/")[-1]
            name = os.path.splitext(name)[0]
            colors[name] = fn
        return colors

    @staticmethod
    def get_fonts(font_dir: str) -> dict[str, str]:
        """Grabs all color YAML filenames from the supplied `font_dir`

        Parameters
        ----------
        font_dir:
            String of the absolute path to the directory where alacritty
            font options are stored as YAML files

        Returns
        -------
        fonts:
            Dictionary where the font file basenames are keys and the associated
            absolute file paths are the values
        """

        font_files = sorted(glob("{}/*.yml".format(font_dir)))
        fonts = {}
        for fn in font_files:
            name = fn.split("/")[-1]
            name = os.path.splitext(name)[0]
            fonts[name] = fn
        return fonts

    @staticmethod
    def _validate_colors(data: dict) -> Union[None, KeyError]:
        """Checks basic keys of proposed color options"""
        for key in data["colors"].keys():
            try:
                assert key in AlacrittyContainer._color_options
            except:
                return KeyError("{} not acceptable Alacritty color option.".format(key))
        return None

    @staticmethod
    def _validate_fonts(data: dict) -> Union[None, KeyError]:
        """Checks basic keys of proposed font options"""
        for key in data["font"].keys():
            try:
                assert key in AlacrittyContainer._font_options
            except:
                return KeyError("{} not acceptable Alacritty font option.".format(key))
        return None

    @staticmethod
    def load_yaml(config_fn: str = ALACRITTY_CONFIG) -> dict:
        with open(config_fn, "r") as stream:
            config = yaml.load(stream)
        return config

    @staticmethod
    def dump_yaml(data: dict, config_fn: str = ALACRITTY_CONFIG):
        with open(config_fn, "w") as stream:
            yaml.dump(data, stream)

    def dump_current_alacritty_config(self):
        """Dumps current Alacritty configuration to file"""
        AlacrittyContainer.dump_yaml(self.alacritty_config, self.config_fn)

    def set_colors(self, color_key: str, *args) -> Union[None, BaseException]:
        """Validates a propsed set of color options and, if successful, edits the
        current, loaded Alacritty configuration. The updated configuration is then
        dumped.

        Parameters
        ----------
        color_key:
            Name of the proposed color option, as a key whose value in the color option
            dictionary is the absolute path to the associated color option YAML file.

        Returns
        -------
        None, BaseException
            If the proposed color option is valid, then it is immediately applied. Else,
            A `KeyError` is returned.
        """

        color_fn = self.colors[color_key]
        color_map = AlacrittyContainer.load_yaml(color_fn)
        exception = AlacrittyContainer._validate_colors(color_map)
        if exception != None:
            return exception
        self.alacritty_config["colors"] = color_map["colors"]
        self.dump_current_alacritty_config()

    def set_font(self, font_key: str, *args) -> Union[None, BaseException]:
        """Validates a propsed set of font options and, if successful, edits the
        current, loaded Alacritty configuration. The updated configuration is then
        dumped.

        Parameters
        ----------
        font_key:
            Name of the proposed font option, as a key whose value in the font option
            dictionary is the absolute path to the associated font option YAML file.

        Returns
        -------
        None, BaseException
            If the proposed font option is valid, then it is immediately applied. Else,
            A `KeyError` is returned.
        """

        font_fn = self.fonts[font_key]
        font_map = AlacrittyContainer.load_yaml(font_fn)
        exception = AlacrittyContainer._validate_fonts(font_map)
        if exception != None:
            raise exception
        self.alacritty_config["font"] = font_map["font"]
        if "draw_bold_text_with_bright_colors" in list(font_map.keys()):
            self.alacritty_config["draw_bold_text_with_bright_colors"] = font_map[
                "draw_bold_text_with_bright_colors"
            ]
        self.dump_current_alacritty_config()

    @staticmethod
    def _validate_opacity(opacity: float) -> bool:
        """Makes sure that the input opacity is a float between 0.0 and 1.0, inclusive"""
        if (opacity < 0) or (opacity > 1):
            return False
        else:
            return True

    def set_opacity(self, opacity: float) -> Union[None, BaseException]:
        """Validates a propsed background window opacity and, if successful, edits the
        current, loaded Alacritty configuration. The updated configuration is then
        dumped.

        Parameters
        ----------
        opacity:
            Proposed background window opacity, which should be a float between 0.0
            and 1.0 inclusive.

        Returns
        -------
        None, BaseException
            If the proposed opacity is valid, then it is immediately applied. Else,
            A `KeyError` is returned.
        """

        if AlacrittyContainer._validate_opacity(opacity):
            self.alacritty_config["window"]["opacity"] = opacity
            self.dump_current_alacritty_config()
        else:
            return ValueError("Opacity {} is not valid.".format(opacity))
