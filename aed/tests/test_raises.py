from aed.container.alacritty_container import (
    AlacrittyContainer,
    ALACRITTY_CONFIG,
    ALACRITTY_FONT_DIR,
    ALACRITTY_COLOR_DIR,
)
import pytest
import os


color_validator = lambda container, data: container._validate_colors(data)
font_validator = lambda container, data: container._validate_fonts(data)
opacity_validator = lambda container, data: container._validate_opacity(data)

font_data = {"font": {"weird_key": "weird_value"}}
color_data = {"font": {"weird_key": "weird_value"}}

ac = AlacrittyContainer(ALACRITTY_CONFIG, ALACRITTY_COLOR_DIR, ALACRITTY_FONT_DIR)


@pytest.mark.parametrize(
    "container, validator, data, expected_exception",
    [
        (ac, color_validator, color_data, KeyError),
        (ac, font_validator, font_data, KeyError),
        (ac, opacity_validator, -1, ValueError),
        (ac, opacity_validator, 2, ValueError),
    ],
)
def test_alacritty_unknown_key(container, validator, data, expected_exception):
    with pytest.raises(expected_exception):
        raise validator(container, data)
