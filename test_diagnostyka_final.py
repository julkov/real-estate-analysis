import pandas as pd
import numpy as np
import pytest

import crawler_model_diagnostyka_final as rs


@pytest.mark.parametrize(
    "photos, expected",
    [
        ([], 0),
        (["photo.jpg"], 1),
        (["photo1.jpg", "photo2.jpg"], 2),
        (None, 0),
    ],
    ids=["empty", "one_photo", "two_photos", "none"],
)
def test_load_data_should_count_photos(monkeypatch, photos, expected):
    df = pd.DataFrame(
        {
            "photos": [photos],
            "price": [2000],
            "surface": [40],
        }
    )

    monkeypatch.setattr(rs.pd, "read_parquet", lambda x: df.copy())

    result = rs.load_data()

    assert result["photos_number"].iloc[0] == expected


def test_load_data_should_remove_record_1984(monkeypatch):
    df = pd.DataFrame(
        {
            "photos": [["photo.jpg"], ["photo.jpg"]],
            "price": [2000, 2500],
            "surface": [40, 50],
        },
        index=[1984, 1985],
    )

    monkeypatch.setattr(rs.pd, "read_parquet", lambda x: df.copy())

    result = rs.load_data()

    assert 1984 not in result.index
    assert 1985 in result.index


def test_select_columns_should_return_four_columns():
    df = pd.DataFrame(
        {
            "city": ["Katowice"],
            "price": [2000],
            "type": ["flat"],
            "surface": [40],
            "extra": [123],
        }
    )

    result = rs.select_columns(df)

    assert list(result.columns) == ["city", "price", "type", "surface"]


def test_process_categorical_data_should_create_top_cities_column():
    df = pd.DataFrame(
        {
            "city": ["Katowice", "Katowice", "Krakow"],
            "price": [2000, 2500, 3000],
            "type": ["flat", "flat", "house"],
            "surface": [40, 50, 60],
        }
    )

    result = rs.process_categorical_data(df)

    assert "top_cities" in result.columns
    assert "city" not in result.columns


def test_process_categorical_data_should_change_rare_city_to_other():
    cities = ["Katowice"] * 3 + ["Krakow"] * 2 + ["Warsaw"]

    df = pd.DataFrame(
        {
            "city": cities,
            "price": [2000] * 6,
            "type": ["flat"] * 6,
            "surface": [40] * 6,
        }
    )

    result = rs.process_categorical_data(df)

    assert result["top_cities"].iloc[-1] == "Warsaw"


def test_one_hot_encode_should_create_city_columns():
    df = pd.DataFrame(
        {
            "top_cities": ["Katowice", "Krakow"],
            "price": [2000, 3000],
            "type": ["flat", "house"],
            "surface": [40, 60],
        }
    )

    result = rs.one_hot_encode_categorical_data(df)

    assert "city_Katowice" in result.columns
    assert "city_Krakow" in result.columns
    assert "type_flat" in result.columns
    assert "type_house" in result.columns


def test_one_hot_encode_should_remove_text_columns():
    df = pd.DataFrame(
        {
            "top_cities": ["Katowice"],
            "price": [2000],
            "type": ["flat"],
            "surface": [40],
        }
    )

    result = rs.one_hot_encode_categorical_data(df)

    assert "top_cities" not in result.columns
    assert "type" not in result.columns


def test_create_models_should_return_12_models():
    result = rs.create_models()

    assert len(result) == 12


def test_compare_models_should_return_results():
    x = pd.DataFrame(
        {
            "surface": [30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
        }
    )
    y = np.array([1500, 1800, 2200, 2600, 3000, 3400, 3900, 4300, 4700, 5100])

    models = [
        ("Linear Regression", rs.LinearRegression()),
    ]

    result = rs.compare_models(x, y, models)

    assert "Linear Regression" in result.index
    assert "RMSE test" in result.columns
    assert "MAE test" in result.columns
    assert "R2 test" in result.columns


def test_data_preparation_and_model_comparison_should_work():
    df = pd.DataFrame(
        {
            "city": ["Katowice", "Krakow", "Warsaw", "Gdansk", "Lodz"],
            "price": [2000, 3000, 2500, 2200, 2800],
            "type": ["flat", "house", "flat", "flat", "house"],
            "surface": [40, 60, 50, 45, 55],
        }
    )

    selected = rs.select_columns(df)
    processed = rs.process_categorical_data(selected)
    encoded = rs.one_hot_encode_categorical_data(processed)

    x = encoded.drop(columns=["price"])
    y = encoded["price"].values

    models = [
        ("Linear Regression", rs.LinearRegression()),
    ]

    result = rs.compare_models(x, y, models)

    assert "price" not in x.columns
    assert "Linear Regression" in result.index
