"""
Rental Scraper - tworzenie modelu regresji i jego diagnostyka

Autor: Julia Kowalczyk

Licencja: MIT
"""

import logging

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import (
    root_mean_squared_error,
    mean_absolute_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from matplotlib.backends.backend_pdf import PdfPages


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


def load_data():
    """
    Wczytuje dane z pliku parquet i przygotowuje liczbę zdjęć
    dla każdej oferty.
    """

    logger.info("Wczytywanie danych z pliku offers_df.parquet")

    try:
        df = pd.read_parquet("offers_df.parquet")

    except Exception:
        logger.exception("Nie udało się wczytać pliku offers_df.parquet")
        raise

    logger.info("Wczytano %d rekordów", len(df))

    df["photos_number"] = df["photos"].apply(
        lambda photos: len(photos) if photos is not None else 0
    )

    logger.info(
        "Dodano kolumnę photos_number. Średnia liczba zdjęć: %.2f",
        df["photos_number"].mean(),
    )

    # Usuwamy rekord (to przypadek skrajny).

    if 1984 in df.index:
        df = df.drop(index=1984)
        logger.info("Usunięto rekord o indeksie 1984")
    else:
        logger.warning(
            "Rekord o indeksie 1984 nie istnieje - nie został usunięty"
        )

    logger.info(
        "Liczba rekordów po przygotowaniu danych: %d",
        len(df),
    )

    return df


def select_columns(df):
    """
    Wybiera kolumny, które będą używane w modelu.
    """

    selected_columns = df[
        ["city", "price", "type", "surface"]
    ]

    logger.info(
        "Wybrano kolumny do modelu: %s",
        list(selected_columns.columns),
    )

    return selected_columns


def process_categorical_data(df):
    """
    Przygotowuje dane dotyczące miast.

    Wybieramy 14 miast, które występują najczęściej.
    Wszystkie pozostałe miasta otrzymują nazwę "other".
    """

    top_cities = (
        df.groupby("city")
        .size()
        .sort_values(ascending=False)
        .head(14)
        .index
        .to_list()
    )

    logger.info(
        "Wybrano %d najpopularniejszych miast",
        len(top_cities),
    )

    logger.debug(
        "Najpopularniejsze miasta: %s",
        top_cities,
    )

    df["top_cities"] = df["city"].apply(
        lambda city: city if city in top_cities else "other"
    )

    # Usuwamy starą kolumnę city.

    df = df.drop(columns=["city"])

    logger.info(
        "Zastąpiono kolumnę city kolumną top_cities"
    )

    return df


def one_hot_encode_categorical_data(df):
    """
    Zamienia dane tekstowe na liczby za pomocą
    One-Hot Encoding.
    """

    cities_encoded = pd.get_dummies(
        df["top_cities"],
        prefix="city",
    )

    type_encoded = pd.get_dummies(
        df["type"],
        prefix="type",
    )

    df_encoded = (
        df.drop(columns=["top_cities", "type"])
        .join(cities_encoded)
        .join(type_encoded)
    )

    logger.info(
        "Wykonano One-Hot Encoding. Liczba kolumn po encodingu: %d",
        df_encoded.shape[1],
    )

    logger.debug(
        "Kolumny po encodingu: %s",
        list(df_encoded.columns),
    )

    return df_encoded


def diagnose_data(df):
    """
    Wykonuje podstawową diagnostykę danych.
    """

    logger.info("Rozpoczęcie diagnostyki danych")

    logger.info(
        "Rozmiar danych: %s",
        df.shape,
    )

    missing_values = df.isnull().sum()

    total_missing = missing_values.sum()

    if total_missing > 0:
        logger.warning(
            "W danych znajduje się %d brakujących wartości",
            total_missing,
        )

        logger.debug(
            "Brakujące wartości według kolumn:\n%s",
            missing_values[missing_values > 0],
        )

    else:
        logger.info("Brak brakujących wartości")

    logger.debug(
        "Typy danych:\n%s",
        df.dtypes,
    )

    logger.debug(
        "Statystyki danych:\n%s",
        df.describe(),
    )

    logger.info(
        "Statystyki ceny:\n%s",
        df["price"].describe(),
    )

    logger.info(
        "Statystyki powierzchni:\n%s",
        df["surface"].describe(),
    )

    correlation = df["surface"].corr(df["price"])

    logger.info(
        "Korelacja surface-price: %.4f",
        correlation,
    )

    logger.info("Zakończono diagnostykę danych")


def create_diagnostic_plots(df, pdf):
    """
    Tworzy podstawowe wykresy diagnostyczne.
    """

    logger.info("Tworzenie wykresów diagnostycznych")

    # Histogram cen

    fig = plt.figure(figsize=(10, 6))

    plt.hist(
        df["price"],
        bins=40,
        rwidth=0.95
    )

    plt.xlabel("Price")
    plt.ylabel("Number of offers")
    plt.title("Distribution of property prices")

    plt.ticklabel_format(
        style="plain",
        axis="x",
    )

    plt.grid(True)

    plt.tight_layout()
    pdf.savefig(fig)
    plt.close(fig)

    # Boxplot cen

    fig = plt.figure(figsize=(8, 4))

    plt.boxplot(df["price"])

    plt.ylabel("Price")
    plt.title("Boxplot of price")

    plt.grid(
        axis="y",
        alpha=0.3,
    )

    pdf.savefig(fig)
    plt.close(fig)

    # Wykres powierzchnia vs cena

    fig = plt.figure(figsize=(8, 5))

    plt.scatter(
        df["surface"],
        df["price"],
        alpha=0.5,
    )

    plt.xlabel("Surface")
    plt.ylabel("Price")
    plt.title("Price vs surface")

    plt.grid(True)

    pdf.savefig(fig)
    plt.close(fig)

    logger.info("Zakończono tworzenie wykresów diagnostycznych")


def create_models():
    """
    Tworzy listę modeli, które będą porównywane.
    """

    return [
        (
            "Linear Regression",
            LinearRegression(),
        ),

        (
            "Random Forest w/ Scaler msl=3",
            make_pipeline(
                StandardScaler(),
                RandomForestRegressor(
                    min_samples_leaf=3
                ),
            ),
        ),

        (
            "Random Forest w/ Scaler msl=5",
            make_pipeline(
                StandardScaler(),
                RandomForestRegressor(
                    min_samples_leaf=5
                ),
            ),
        ),

        (
            "Random Forest w/ Scaler msl=10",
            make_pipeline(
                StandardScaler(),
                RandomForestRegressor(
                    min_samples_leaf=10
                ),
            ),
        ),

        (
            "Random Forest w/ Scaler mss=4",
            make_pipeline(
                StandardScaler(),
                RandomForestRegressor(
                    min_samples_split=4
                ),
            ),
        ),

        (
            "Random Forest w/ Scaler mss=8",
            make_pipeline(
                StandardScaler(),
                RandomForestRegressor(
                    min_samples_split=8
                ),
            ),
        ),

        (
            "Ridge w/ Scaler alpha=1",
            make_pipeline(
                StandardScaler(),
                Ridge(alpha=1),
            ),
        ),

        (
            "Ridge w/ Scaler alpha=0.1",
            make_pipeline(
                StandardScaler(),
                Ridge(alpha=0.1),
            ),
        ),

        (
            "Ridge w/ Scaler alpha=10",
            make_pipeline(
                StandardScaler(),
                Ridge(alpha=10),
            ),
        ),

        (
            "Lasso w/ Scaler alpha=1",
            make_pipeline(
                StandardScaler(),
                Lasso(alpha=1),
            ),
        ),

        (
            "Lasso w/ Scaler alpha=0.1",
            make_pipeline(
                StandardScaler(),
                Lasso(alpha=0.1),
            ),
        ),

        (
            "Lasso w/ Scaler alpha=10",
            make_pipeline(
                StandardScaler(),
                Lasso(alpha=10),
            ),
        ),
    ]


def compare_models(x, y, models):
    """
    Trenuje wszystkie modele i porównuje ich wyniki.
    """

    logger.info(
        "Rozpoczęcie porównywania %d modeli",
        len(models),
    )

    rmses_test = []
    rmses_train = []

    maes_test = []
    maes_train = []

    r2_test = []
    r2_train = []

    # Dzielimy dane tylko raz.
    # Każdy model otrzymuje dokładnie taki sam zbiór treningowy i testowy.

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=0,
    )

    logger.info(
        "Podział danych: train=%d, test=%d",
        len(x_train),
        len(x_test),
    )

    for model_name, model in models:
        logger.info(
            "Trenowanie modelu: %s",
            model_name,
        )

        model.fit(
            x_train,
            y_train,
        )

        y_pred = model.predict(x_test)
        y_pred_train = model.predict(x_train)

        rmse_test = root_mean_squared_error(
            y_test,
            y_pred,
        )

        mae_test = mean_absolute_error(
            y_test,
            y_pred,
        )

        rmse_train = root_mean_squared_error(
            y_train,
            y_pred_train,
        )

        mae_train = mean_absolute_error(
            y_train,
            y_pred_train,
        )

        r2_test_score = r2_score(
            y_test,
            y_pred,
        )

        r2_train_score = r2_score(
            y_train,
            y_pred_train,
        )

        rmses_test.append(rmse_test)
        rmses_train.append(rmse_train)

        maes_test.append(mae_test)
        maes_train.append(mae_train)

        r2_test.append(r2_test_score)
        r2_train.append(r2_train_score)

        logger.info(
            "%s | "
            "RMSE test=%.2f | "
            "RMSE train=%.2f | "
            "MAE test=%.2f | "
            "MAE train=%.2f | "
            "R2 test=%.4f | "
            "R2 train=%.4f",
            model_name,
            rmse_test,
            rmse_train,
            mae_test,
            mae_train,
            r2_test_score,
            r2_train_score,
        )

    results = pd.DataFrame(
        {
            "RMSE test": rmses_test,
            "RMSE train": rmses_train,
            "MAE test": maes_test,
            "MAE train": maes_train,
            "R2 test": r2_test,
            "R2 train": r2_train,
        },
        index=[model_name for model_name, _ in models],
    )

    return results


def plot_model_comparison(results, pdf):
    """
    Tworzy wykres porównujący wyniki modeli
    i zapisuje go do raportu PDF.
    """

    logger.info("Tworzenie wykresu porównującego modele")

    results.plot.bar(rot=90)

    plt.subplots_adjust(bottom=0.3)

    plt.grid(
        axis="y",
        alpha=0.3,
    )

    pdf.savefig(bbox_inches="tight")
    plt.close()


def analyze_training_size(x, y):
    """
    Sprawdza, jak liczba danych treningowych wpływa
    na wyniki modelu Random Forest.
    """

    logger.info(
        "Rozpoczęcie analizy wpływu liczby danych treningowych"
    )

    rfr4_rmses_test = []
    rfr4_rmses_train = []

    rfr4_maes_test = []
    rfr4_maes_train = []

    sample_sizes = [
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1.0,
    ]

    # Tworzymy testowy zbiór danych.

    x_train_full, x_test, y_train_full, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=0,
    )

    for p in sample_sizes:

        x_train = x_train_full
        y_train = y_train_full

        # Jeżeli p jest mniejsze niż 1 zmniejszamy zbiór treningowy.

        if p < 1:
            x_train, _, y_train, _ = train_test_split(
                x_train_full,
                y_train_full,
                test_size=1 - p,
                random_state=42,
            )

        pipe = make_pipeline(
            StandardScaler(),
            RandomForestRegressor(
                min_samples_split=4
            ),
        )

        pipe.fit(
            x_train,
            y_train,
        )

        y_pred = pipe.predict(x_test)
        y_pred_train = pipe.predict(x_train)

        rmse_test = root_mean_squared_error(
            y_test,
            y_pred,
        )

        mae_test = mean_absolute_error(
            y_test,
            y_pred,
        )

        rmse_train = root_mean_squared_error(
            y_train,
            y_pred_train,
        )

        mae_train = mean_absolute_error(
            y_train,
            y_pred_train,
        )

        rfr4_rmses_test.append(rmse_test)
        rfr4_rmses_train.append(rmse_train)

        rfr4_maes_test.append(mae_test)
        rfr4_maes_train.append(mae_train)

        logger.info(
            "Training size=%.0f%% | "
            "RMSE test=%.2f | "
            "RMSE train=%.2f | "
            "MAE test=%.2f | "
            "MAE train=%.2f",
            p * 100,
            rmse_test,
            rmse_train,
            mae_test,
            mae_train,
        )

    return (
        sample_sizes,
        rfr4_rmses_test,
        rfr4_rmses_train,
        rfr4_maes_test,
        rfr4_maes_train,
    )


def plot_training_size_results(
        sample_sizes,
        rmses_test,
        rmses_train,
        maes_test,
        maes_train,
        pdf
):
    """
    Tworzy wykresy pokazujące wpływ liczby danych treningowych
    na RMSE i MAE.
    """

    logger.info(
        "Tworzenie wykresów wpływu liczby danych treningowych"
    )

    fig, ax = plt.subplots(1, 2)

    ax[0].plot(
        sample_sizes,
        rmses_test,
        label="test",
    )

    ax[0].plot(
        sample_sizes,
        rmses_train,
        label="train",
    )

    ax[0].set_title("Root Mean Squared Error")
    ax[0].set_xlabel("sample size")
    ax[0].set_ylim([0, None])
    ax[0].legend()

    ax[1].plot(
        sample_sizes,
        maes_test,
        label="test",
    )

    ax[1].plot(
        sample_sizes,
        maes_train,
        label="train",
    )

    ax[1].set_title("Mean Absolute Error")
    ax[1].set_xlabel("sample size")
    ax[1].set_ylim([0, None])
    ax[1].legend()

    pdf.savefig(fig)
    plt.close(fig)


def evaluate_best_model(x, y, pdf):
    """
    Szczegółowa diagnostyka modelu Random Forest
    z min_samples_split=4.

    Funkcja:
    - dzieli dane na train/test,
    - trenuje model,
    - oblicza RMSE, MAE i R2 dla train i test,
    - porównuje wyniki train/test,
    - sprawdza możliwość overfittingu,
    - analizuje reszty,
    - tworzy wykresy diagnostyczne,
    - tworzy tabelę rzeczywistych i przewidywanych wartości.

    Zwraca:
    - wytrenowany model,
    - słownik z wynikami diagnostyki.
    """

    logger.info(
        "Rozpoczęcie szczegółowej diagnostyki "
        "Random Forest min_samples_split=4"
    )

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=0,
    )

    logger.info(
        "Podział danych: train=%d, test=%d",
        len(x_train),
        len(x_test),
    )

    model = make_pipeline(
        StandardScaler(),
        RandomForestRegressor(
            min_samples_split=4
        ),
    )

    logger.info(
        "Utworzono Random Forest z min_samples_split=4"
    )

    model.fit(
        x_train,
        y_train,
    )

    logger.info(
        "Zakończono trening modelu"
    )

    y_pred_train = model.predict(x_train)
    y_pred_test = model.predict(x_test)

    rmse_train = root_mean_squared_error(
        y_train,
        y_pred_train,
    )

    mae_train = mean_absolute_error(
        y_train,
        y_pred_train,
    )

    r2_train = r2_score(
        y_train,
        y_pred_train,
    )

    rmse_test = root_mean_squared_error(
        y_test,
        y_pred_test,
    )

    mae_test = mean_absolute_error(
        y_test,
        y_pred_test,
    )

    r2_test = r2_score(
        y_test,
        y_pred_test,
    )

    rmse_difference = rmse_test - rmse_train
    mae_difference = mae_test - mae_train
    r2_difference = r2_train - r2_test

    logger.info(
        "Random Forest mss=4 | "
        "RMSE train=%.2f | RMSE test=%.2f",
        rmse_train,
        rmse_test,
    )

    logger.info(
        "Random Forest mss=4 | "
        "MAE train=%.2f | MAE test=%.2f",
        mae_train,
        mae_test,
    )

    logger.info(
        "Random Forest mss=4 | "
        "R2 train=%.4f | R2 test=%.4f",
        r2_train,
        r2_test,
    )

    logger.info(
        "Różnica RMSE test-train = %.2f",
        rmse_difference,
    )

    logger.info(
        "Różnica MAE test-train = %.2f",
        mae_difference,
    )

    logger.info(
        "Różnica R2 train-test = %.4f",
        r2_difference,
    )

    if r2_difference > 0.10:

        logger.warning(
            "Model może być przeuczony. "
            "Różnica R2 train-test = %.4f",
            r2_difference,
        )

    else:

        logger.info(
            "Nie wykryto dużej różnicy R2 train-test. "
            "Różnica = %.4f",
            r2_difference,
        )

    residuals = y_test - y_pred_test

    mean_residual = np.mean(residuals)
    std_residual = np.std(residuals)

    logger.info(
        "Średnia reszt = %.2f",
        mean_residual,
    )

    logger.info(
        "Odchylenie standardowe reszt = %.2f",
        std_residual,
    )

    logger.info(
        "Tworzenie wykresu Actual vs Predicted"
    )

    fig = plt.figure(figsize=(7, 7))

    plt.scatter(
        y_test,
        y_pred_test,
        alpha=0.5,
    )

    minimum = min(
        y_test.min(),
        y_pred_test.min(),
    )

    maximum = max(
        y_test.max(),
        y_pred_test.max(),
    )

    plt.plot(
        [minimum, maximum],
        [minimum, maximum],
    )

    plt.xlabel("Cena rzeczywista")
    plt.ylabel("Cena przewidywana")

    plt.title(
        "Random Forest mss=4 - rzeczywiste vs przewidywane"
    )

    plt.grid(True)

    plt.tight_layout()

    pdf.savefig(fig)
    plt.close(fig)

    logger.info(
        "Tworzenie wykresu Residuals vs Predicted"
    )

    fig = plt.figure(figsize=(7, 5))

    plt.scatter(
        y_pred_test,
        residuals,
        alpha=0.5,
    )

    plt.axhline(
        0,
        linestyle="--",
    )

    plt.xlabel("Cena przewidywana")

    plt.ylabel(
        "Reszta (rzeczywista - przewidywana)"
    )

    plt.title(
        "Random Forest mss=4 - wykres reszt"
    )

    plt.grid(True)

    plt.tight_layout()

    pdf.savefig(fig)
    plt.close(fig)

    logger.info(
        "Tworzenie histogramu reszt"
    )

    fig = plt.figure(figsize=(7, 5))

    plt.hist(
        residuals,
        bins=30,
    )

    plt.axvline(
        0,
        linestyle="--",
    )

    plt.xlabel("Reszta")

    plt.ylabel(
        "Liczba obserwacji"
    )

    plt.title(
        "Random Forest mss=4 - histogram reszt"
    )

    plt.grid(True)

    plt.tight_layout()

    pdf.savefig(fig)
    plt.close(fig)

    comparison = pd.DataFrame(
        {
            "cena_rzeczywista": y_test,
            "cena_przewidywana": y_pred_test,
            "blad": residuals,
        }
    )

    logger.info(
        "Utworzono tabelę porównującą wartości rzeczywiste "
        "i przewidywane"
    )

    logger.info(
        "Przykładowe predykcje:\n%s",
        comparison.head(10),
    )

    diagnostics = {
        "RMSE_train": rmse_train,
        "RMSE_test": rmse_test,
        "MAE_train": mae_train,
        "MAE_test": mae_test,
        "R2_train": r2_train,
        "R2_test": r2_test,
        "RMSE_difference": rmse_difference,
        "MAE_difference": mae_difference,
        "R2_difference": r2_difference,
        "mean_residual": mean_residual,
        "std_residual": std_residual,
        "comparison": comparison,
    }

    logger.info(
        "Zakończono szczegółową diagnostykę "
        "Random Forest min_samples_split=4"
    )

    return model, diagnostics


def save_models(x, y):
    """
    Trenuje modele na wszystkich dostępnych danych
    i zapisuje je do plików.
    """

    logger.info(
        "Rozpoczęcie trenowania modeli przeznaczonych do zapisu"
    )

    # Random Forest

    model = make_pipeline(
        StandardScaler(),
        RandomForestRegressor(
            min_samples_split=4
        ),
    )

    logger.info("Trenowanie Random Forest na wszystkich danych")

    model.fit(
        x,
        y,
    )

    # Linear Regression

    model2 = LinearRegression()

    logger.info(
        "Trenowanie Linear Regression na wszystkich danych"
    )

    model2.fit(
        x,
        y,
    )

    # Zapis Random Forest

    try:

        joblib.dump(
            model,
            "my_random_forest_final.joblib",
        )

        logger.info(
            "Zapisano Random Forest: my_random_forest_final.joblib"
        )

    except Exception:
        logger.exception(
            "Nie udało się zapisać Random Forest"
        )
        raise

    # Zapis Linear Regression

    try:

        joblib.dump(
            model2,
            "my_linear_regression_final.joblib",
        )

        logger.info(
            "Zapisano Linear Regression: "
            "my_linear_regression_final.joblib"
        )

    except Exception:
        logger.exception(
            "Nie udało się zapisać Linear Regression"
        )
        raise


def main():
    """
    Główna funkcja programu.
    """

    logger.info("START PROGRAMU")

    df = load_data()

    selected_df = select_columns(df)

    processed_df = process_categorical_data(
        selected_df
    )

    df_encoded = one_hot_encode_categorical_data(
        processed_df
    )

    logger.debug(
        "Pierwszy rekord po encodingu: %s",
        df_encoded.iloc[0].to_dict(),
    )

    diagnose_data(df_encoded)

    with PdfPages("regression_report.pdf") as pdf:

        create_diagnostic_plots(
            df_encoded,
            pdf,
        )

        x = df_encoded.drop(
            columns=["price"]
        )

        y = df_encoded["price"].values.ravel()

        logger.info(
            "Przygotowano X i y: X=%s, y=%s",
            x.shape,
            y.shape,
        )

        models = create_models()

        best_model_name = "Random Forest w/ Scaler mss=4"

        results = compare_models(
            x,
            y,
            models,
        )

        logger.info(
            "Wybrany model do dalszej ewaluacji: %s",
            best_model_name,
        )

        logger.info(
            "Wyniki porównania modeli:\n%s",
            results,
        )

        plot_model_comparison(
            results,
            pdf,
        )

        (
            sample_sizes,
            rmses_test,
            rmses_train,
            maes_test,
            maes_train,
        ) = analyze_training_size(
            x,
            y,
        )

        plot_training_size_results(
            sample_sizes,
            rmses_test,
            rmses_train,
            maes_test,
            maes_train,
            pdf,
        )

        best_model, diagnostics = evaluate_best_model(
            x,
            y,
            pdf,
        )

        logger.info(
            "PODSUMOWANIE DIAGNOSTYKI MODELU mss=4:"
        )

        logger.info(
            "RMSE train = %.2f",
            diagnostics["RMSE_train"],
        )

        logger.info(
            "RMSE test = %.2f",
            diagnostics["RMSE_test"],
        )

        logger.info(
            "MAE train = %.2f",
            diagnostics["MAE_train"],
        )

        logger.info(
            "MAE test = %.2f",
            diagnostics["MAE_test"],
        )

        logger.info(
            "R2 train = %.4f",
            diagnostics["R2_train"],
        )

        logger.info(
            "R2 test = %.4f",
            diagnostics["R2_test"],
        )

        logger.info(
            "Różnica R2 train-test = %.4f",
            diagnostics["R2_difference"],
        )

        logger.info(
            "Średnia reszt=%.2f",
            diagnostics["mean_residual"],
        )

        logger.info(
            "STD reszt=%.2f",
            diagnostics["std_residual"],
        )

        save_models(
            x,
            y,
        )

    logger.info("KONIEC PROGRAMU")


if __name__ == "__main__":

    try:
        main()

    except Exception:
        logger.exception(
            "Program zakończył się błędem"
        )
        raise
