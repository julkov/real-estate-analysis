import flet as ft
from crawler_GUI_final import create_dropdown, create_surface_field
import pytest


def test_create_dropdown_creates_dropdown():
    options = ["warsaw", "krakow", "gdansk"]

    dropdown = create_dropdown("City", options)

    assert isinstance(dropdown, ft.Dropdown)
    assert dropdown.label == "City"
    assert len(dropdown.options) == 3


def test_create_dropdown_changes_option_text():
    options = ["new_york", "los_angeles"]

    dropdown = create_dropdown("City", options)

    assert dropdown.options[0].text == "New York"
    assert dropdown.options[1].text == "Los Angeles"


def test_create_dropdown_preserves_option_keys():
    options = ["warsaw", "krakow"]

    dropdown = create_dropdown("City", options)

    assert dropdown.options[0].key == "warsaw"
    assert dropdown.options[1].key == "krakow"


def test_create_surface_field_returns_text_field_and_row():
    surface_input, surface_row = create_surface_field()

    assert isinstance(surface_input, ft.TextField)
    assert isinstance(surface_row, ft.Row)


def test_create_surface_field_has_square_meter_unit():
    surface_input, surface_row = create_surface_field()

    assert len(surface_row.controls) == 2
    assert surface_row.controls[1].value == "m²"


def test_create_surface_field_has_correct_label():
    surface_input, surface_row = create_surface_field()

    assert surface_input.label == "Surface area"


@pytest.mark.parametrize(
    "option, expected_text",
    [
        ("apartment", "Apartment"),
        ("house", "House"),
        ("semi_detached_house", "Semi Detached House"),
        ("student_room", "Student Room"),
    ],
    ids=[
        "apartment",
        "house",
        "semi-detached-house",
        "student-room",
    ],
)
def test_create_dropdown_formats_option_text(option, expected_text):
    dropdown = create_dropdown("Property type", [option])

    assert dropdown.options[0].text == expected_text
