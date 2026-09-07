"""
Rental Scraper - interfejs graficzny aplikacji

Autor: Julia Kowalczyk

Licencja: MIT
"""


import flet as ft
from model_final import Model


# Funkcje pomocnicze


def create_dropdown(title, options):
    """
    Tworzy pola wyboru (Dropdown).
    """
    dropdown = ft.Dropdown(
        label=title,
        hint_text=f"Select {title.lower()}",
        width=460,
        options=[
            ft.DropdownOption(
                key=option,
                text=option.replace("_", " ").title(),
            )
            for option in options
        ],
    )

    return dropdown


def create_surface_field():
    """
    Tworzy pole do wpisania powierzchni.
    """
    surface_input = ft.TextField(
        label="Surface area",
        hint_text="Enter surface area",
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.NumbersOnlyInputFilter(),
        width=420,
    )

    surface_unit = ft.Text(
        "m²",
        size=16,
    )

    surface_row = ft.Row(
        controls=[
            surface_input,
            surface_unit,
        ],
        spacing=10,
    )

    return surface_input, surface_row


def main(page: ft.Page):
    """
    Główna aplikacja.

    Funkcja odpowiada za:

    - ustawienie strony,
    - wczytanie modeli,
    - pobranie nazw cech z modelu,
    - utworzenie pól formularza,
    - wyświetlenie komunikatu błędu,
    - wyświetlenie wyniku predykcji.
    """

    page.title = "Real Estate Price Predictor"

    page.padding = 30

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.bgcolor = "#F3F6FA"


    random_forest_model = Model(
        path="../../PythonZajęcia/my_random_forest_2.joblib"
    )

    linear_regression_model = Model(
        path="../../PythonZajęcia/my_linear_regression_2.joblib"
    )


    cities = []
    types = []

    for feature in random_forest_model.feature_names():

        if feature.startswith("city_"):
            cities.append(feature[5:])

        elif feature.startswith("type_"):
            types.append(feature[5:])


    city_select = create_dropdown(
        "City",
        cities
    )

    type_select = create_dropdown(
        "Property type",
        types
    )

    surface_input, surface_row = create_surface_field()


    error_message = ft.Text(
        "",
        size=14,
    )


    result_title = ft.Text(
        "Estimated monthly rent",
        size=20,
        weight=ft.FontWeight.BOLD,
    )

    random_forest_result = ft.Text(
        "",
        size=18,
    )

    linear_regression_result = ft.Text(
        "",
        size=15,
    )

    result_container = ft.Container(
        content=ft.Column(
            controls=[
                result_title,
                ft.Divider(),
                random_forest_result,
                linear_regression_result,
            ],
            spacing=10,
        ),
        padding=20,
        bgcolor="#FFFFFF",
        border_radius=12,
        visible=False,
    )


    def validate_surface(e):

        value = surface_input.value

        if not value:
            surface_input.error_text = None
            error_message.value = ""
            page.update()
            return

        try:
            surface = int(value)

        except ValueError:
            surface_input.error_text = "Enter a valid number."
            page.update()
            return

        if surface <= 10:
            surface_input.error_text = (
                "Surface area must be greater than 10 m²."
            )

        elif surface > 300:
            surface_input.error_text = (
                "Surface area cannot be greater than 300 m²."
            )

        else:
            surface_input.error_text = None

        page.update()

    surface_input.on_change = validate_surface


    def predict(e):

        error_message.value = ""
        result_container.visible = False


        if city_select.value is None:
            error_message.value = "Please select a city."
            page.update()
            return


        if type_select.value is None:
            error_message.value = "Please select a property type."
            page.update()
            return


        if not surface_input.value:
            surface_input.error_text = "Please enter the surface area."
            page.update()
            return

        try:
            surface = int(surface_input.value)

        except ValueError:
            surface_input.error_text = "Enter a valid number."
            page.update()
            return

        if surface <= 10:
            surface_input.error_text = (
                "Surface area must be greater than 10 m²."
            )
            page.update()
            return

        if surface > 300:
            surface_input.error_text = (
                "Surface area cannot be greater than 300 m²."
            )
            page.update()
            return

        surface_input.error_text = None


        cities_one_hot = []

        for city in cities:

            if city == city_select.value:
                cities_one_hot.append(1)
            else:
                cities_one_hot.append(0)


        types_one_hot = []

        for type_ in types:

            if type_ == type_select.value:
                types_one_hot.append(1)
            else:
                types_one_hot.append(0)


        features = (
            [surface]
            + cities_one_hot
            + types_one_hot
        )


        try:

            linear_prediction = (
                linear_regression_model
                .predict(features)[0]
            )

            random_forest_prediction = (
                random_forest_model
                .predict(features)[0]
            )

        except Exception as ex:

            error_message.value = (
                f"Prediction error: {ex}"
            )

            page.update()
            return


        random_forest_result.value = (
            f"Random Forest: "
            f"{random_forest_prediction:,.2f} € / month"
        )

        linear_regression_result.value = (
            f"Linear Regression: "
            f"{linear_prediction:,.2f} € / month"
        )

        result_container.visible = True

        page.update()


    def clear_form(e):

        city_select.value = None
        type_select.value = None

        surface_input.value = ""
        surface_input.error_text = None

        error_message.value = ""

        random_forest_result.value = ""
        linear_regression_result.value = ""

        result_container.visible = False

        page.update()


    prediction_button = ft.Button(
        content="Predict price",
        on_click=predict,
    )

    clear_button = ft.Button(
        content="Clear",
        on_click=clear_form,
    )

    buttons_row = ft.Row(
        controls=[
            prediction_button,
            clear_button,
        ],
        spacing=10,
    )


    header = ft.Column(
        controls=[
            ft.Text(
                "Real Estate Price Predictor",
                size=28,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Text(
                "Estimate the monthly rental price of a property",
                size=15,
            ),
        ],
        spacing=5,
    )


    form = ft.Container(
        content=ft.Column(
            controls=[
                header,

                ft.Divider(),

                city_select,

                type_select,

                surface_row,

                error_message,

                buttons_row,

                result_container,
            ],
            spacing=16,
        ),
        width=540,
        padding=30,
        bgcolor="#FFFFFF",
        border_radius=16,
    )


    page.add(form)


# Uruchomienie aplikacji


if __name__ == "__main__":
    ft.run(main)
