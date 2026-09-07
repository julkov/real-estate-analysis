"""
Rental Scraper - eksploracyjna analiza zescrapowanych danych

Autor: Julia Kowalczyk

Licencja: MIT
"""

import pandas as pd


def read_data(file_path):
    """
    Wczytuje dane z pliku Parquet i zwraca je w postaci DataFrame.
    """
    return pd.read_parquet(file_path)


def basic_information(df):
    """
    Oblicza podstawowe informacje o zbiorze danych.

    Funkcja określa liczbę wierszy i kolumn oraz generuje
    podstawowe statystyki opisowe dla kolumn numerycznych.
    """
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "describe": df.describe()
    }


def remove_unnecessary_columns(df):
    """
    Usuwa kolumny, które nie są potrzebne do dalszej analizy.

    W tym przypadku usuwana jest kolumna 'photos'.
    """
    return df.drop(columns=["photos"])


def analyze_missing_and_unique_values(df):
    """
    Analizuje liczbę unikalnych i brakujących wartości w kolumnach.

    Dla każdej kolumny obliczana jest liczba unikalnych wartości,
    liczba brakujących wartości oraz procent brakujących danych.
    """
    missing_values = df.isnull().sum()
    missing_percentage = (missing_values / len(df) * 100).round(2)

    return {
        "unique_values": df.nunique(),
        "missing_values": missing_values,
        "missing_percentage": missing_percentage
    }


def analyze_locations(df):
    """
    Analizuje informacje dotyczące lokalizacji ofert.

    Funkcja określa liczbę unikalnych miast i ulic oraz
    zwraca 10 miast z największą liczbą ofert i ich udział procentowy.
    """
    city_counts = df["city"].value_counts()

    return {
        "number_of_cities": df["city"].nunique(),
        "number_of_streets": df["street"].nunique(),
        "top_cities": city_counts.head(10),
        "top_cities_percentage": (
                df["city"].value_counts(normalize=True).head(10) * 100
        )
    }


def analyze_apartment_types(df):
    """
    Analizuje typy mieszkań oraz ich stan umeblowania.

    Funkcja zwraca liczbę ofert dla poszczególnych typów mieszkań
    oraz liczbę mieszkań umeblowanych, nieumeblowanych i brakujących danych.
    """
    return {
        "types": df["type"].value_counts(),
        "furnished": df["furnished"].value_counts(dropna=False)
    }


def find_price_outliers(df):
    """
    Wyszukuje wartości odstające w kolumnie 'price' metodą IQR.
    """
    q1 = df["price"].quantile(0.25)
    q3 = df["price"].quantile(0.75)
    iqr = q3 - q1

    outliers = df[
        (df["price"] < q1 - 1.5 * iqr) |
        (df["price"] > q3 + 1.5 * iqr)
        ]

    return {
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "outliers": outliers,
        "number_of_outliers": len(outliers)
    }


def analyze_average_prices(df):
    """
    Oblicza średnie ceny mieszkań w zależności od miasta i liczby pokoi.
    """
    return {
        "average_price_by_city": (
            df.groupby("city")["price"]
            .mean()
            .sort_values(ascending=False)
        ),
        "average_price_by_rooms": (
            df.groupby("rooms")["price"].mean()
        )
    }


def calculate_price_per_m2(df):
    """
    Oblicza cenę jednego metra kwadratowego dla każdej oferty.

    Nowa kolumna 'price_per_m2' jest tworzona na podstawie
    ceny mieszkania i jego powierzchni.
    """
    df = df.copy()
    df["price_per_m2"] = df["price"] / df["surface"]

    return df


def analyze_nearby_services(df):
    """
    Analizuje dostępność wybranych usług i obiektów w pobliżu mieszkań.

    Funkcja zlicza oferty znajdujące się w pobliżu szkoły, szpitala,
    transportu publicznego oraz innych usług.
    """
    columns = [
        "near_school",
        "near_hospital",
        "near_public_transport",
        "near_services"
    ]

    return df[columns].sum()


def calculate_correlations(df):
    """
    Oblicza korelacje pomiędzy numerycznymi zmiennymi w zbiorze danych.
    """
    return df.corr(numeric_only=True)


def create_report(df):
    """
    Tworzy kompletny raport z analizy danych.

    Funkcja wykonuje wszystkie etapy analizy i zapisuje ich wyniki
    oraz krótkie opisy do pliku 'analysis_report.txt'.
    """

    report = []

    # Podstawowe informacje
    basic = basic_information(df)

    report.append("PODSTAWOWE INFORMACJE O DANYCH")
    report.append(
        f"Liczba wierszy: {basic['rows']}"
    )
    report.append(
        f"Liczba kolumn: {basic['columns']}"
    )
    report.append(
        "\nPodstawowe statystyki opisowe:"
    )
    report.append(
        str(basic["describe"])
    )

    # Usuwanie kolumny
    report.append("\nUSUWANIE NIEPOTRZEBNEJ KOLUMNY")
    report.append(
        "Kolumna 'photos' została usunięta, ponieważ "
        "nie jest potrzebna do dalszej analizy."
    )

    df = remove_unnecessary_columns(df)

    # Unikalne i brakujące wartości
    missing = analyze_missing_and_unique_values(df)

    report.append("\nUNIKALNE I BRAKUJĄCE WARTOŚCI")

    report.append("\nLiczba unikalnych wartości:")
    report.append(str(missing["unique_values"]))

    report.append("\nLiczba brakujących wartości:")
    report.append(str(missing["missing_values"]))

    report.append("\nProcent brakujących wartości:")
    report.append(str(missing["missing_percentage"]))

    # Lokalizacje
    locations = analyze_locations(df)

    report.append("\n LOKALIZACJE")
    report.append(
        f"Liczba unikalnych miast: "
        f"{locations['number_of_cities']}"
    )
    report.append(
        f"Liczba unikalnych ulic: "
        f"{locations['number_of_streets']}"
    )

    report.append("\n10 miast z największą liczbą ofert:")
    report.append(str(locations["top_cities"]))

    report.append("\nUdział procentowy 10 najczęściej występujących miast:")
    report.append(str(locations["top_cities_percentage"].round(2)))

    # Typy mieszkań
    apartment_types = analyze_apartment_types(df)

    report.append("\nTYPY MIESZKAŃ")
    report.append("\nRozkład typów mieszkań:")
    report.append(str(apartment_types["types"]))

    report.append("\nRozkład umeblowania:")
    report.append(str(apartment_types["furnished"]))

    # Wartości odstające
    outlier_results = find_price_outliers(df)

    report.append("\nWARTOŚCI ODSTAJĄCE")
    report.append(
        f"Pierwszy kwartyl (Q1): {outlier_results['q1']:.2f}"
    )
    report.append(
        f"Trzeci kwartyl (Q3): {outlier_results['q3']:.2f}"
    )
    report.append(
        f"Rozstęp ćwiartkowy (IQR): {outlier_results['iqr']:.2f}"
    )
    report.append(
        f"Liczba wartości odstających: "
        f"{outlier_results['number_of_outliers']}"
    )

    report.append("\nWartości odstające:")
    report.append(str(outlier_results["outliers"]))

    # Średnie ceny
    prices = analyze_average_prices(df)

    report.append("\nŚREDNIE CENY")
    report.append("\nŚrednia cena mieszkań w poszczególnych miastach:")
    report.append(str(prices["average_price_by_city"].round(2)))

    report.append("\nŚrednia cena w zależności od liczby pokoi:")
    report.append(str(prices["average_price_by_rooms"].round(2)))

    # Cena za m2
    df = calculate_price_per_m2(df)

    report.append("\nCENA ZA METR KWADRATOWY")
    report.append(
        "Cena za metr kwadratowy została obliczona jako "
        "cena mieszkania podzielona przez jego powierzchnię."
    )
    report.append("\nPodstawowe statystyki ceny za m²:")
    report.append(str(df["price_per_m2"].describe().round(2)))

    # Udogodnienia
    nearby = analyze_nearby_services(df)

    report.append("\nUDOGODNIENIA W POBLIŻU")
    report.append(
        "Liczba ofert znajdujących się w pobliżu poszczególnych "
        "obiektów i usług:"
    )
    report.append(str(nearby))

    # Korelacje
    correlations = calculate_correlations(df)

    report.append("\nKORELACJE")
    report.append(
        "Macierz korelacji pomiędzy zmiennymi numerycznymi:"
    )
    report.append(str(correlations))

    # Zapis raportu
    with open("analysis_report.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(report))


def main():
    """
    Uruchamia cały proces analizy danych.

    Funkcja wczytuje dane z pliku Parquet, wykonuje analizę
    oraz zapisuje jej wyniki do pliku tekstowego.
    """
    df = read_data("offers_df.parquet")
    create_report(df)


if __name__ == "__main__":
    main()
