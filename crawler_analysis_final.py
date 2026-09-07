import pandas as pd
import matplotlib.pyplot as plt


def read_data():
    df = pd.read_parquet("offers_df.parquet")
    return df


def show_distribution(df, column_name, bins):
    fig, ax = plt.subplots()
    ax.hist(df[column_name], bins=bins)
    ax.set_title(f"{column_name} distribution")
    plt.show()


def show_city_distribution(df):
    occur = df.groupby("city").size().to_frame("city_count")
    filtered_occur = occur[occur["city_count"] >= 20]
    print(filtered_occur)

    fig, ax = plt.subplots()
    ax.bar(filtered_occur.index, filtered_occur["city_count"])
    ax.set_title("city distribution")
    ax.tick_params("x", rotation=45, rotation_mode="xtick")
    plt.show()


def show_house_type_distribution(df):
    occur = df.groupby("type").size().to_frame("type_count")
    filtered_occur = occur[occur["type_count"] >= 3]
    fig, ax = plt.subplots()
    ax.bar(filtered_occur.index, filtered_occur["type_count"])
    ax.set_title("house type distribution")
    ax.tick_params("x", rotation=45, rotation_mode="xtick")
    plt.show()


def show_if_furnished(df):
    occur = df.groupby("furnished").size().to_frame("count")
    filtered_occur = occur[occur["count"] >= 3]
    fig, ax = plt.subplots()
    ax.bar(filtered_occur.index, filtered_occur["count"])
    ax.set_title("furnished/not-furnished")
    ax.set_xticklabels(["furnished", "unfurnished"], rotation=45)
    ax.tick_params("x", rotation=45, rotation_mode="xtick")
    plt.show()
