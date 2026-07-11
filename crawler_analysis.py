import pandas as pd
import numpy as np
from matplotlib.pyplot import title
from sklearn.linear_model import LinearRegression
import csv
import matplotlib.pyplot as plt


def read_data():
    df = pd.read_parquet("offers_df.parquet")
    return df

# print(df.head(10))
# print(df[["city", "street", "price", "rooms", "surface"]])
# print(df.isna().sum())
# print(df.describe().round(4))
# print(df.groupby('city').size())


def show_distribution(df, column_name, bins):
    fig, ax = plt.subplots()
    ax.hist(df[column_name], bins=bins)
    ax.set_title(f"{column_name} distribution")
    ax.set_xlim(1, 500)
    plt.show()


def show_city_distribution(df):
    occur = df.groupby("city").size().to_frame("city_count")
    filtered_occur = occur[occur["city_count"] >= 20]
    # print(filtered_occur)

    fig, ax = plt.subplots()
    ax.bar(filtered_occur.index, filtered_occur["city_count"])
    ax.set_title(f"city distribution")
    ax.tick_params("x", rotation=45, rotation_mode="xtick")
    plt.show()


def show_house_type_distribution(df):
    occur = df.groupby("type").size().to_frame("type_count")
    filtered_occur = occur[occur["type_count"] >= 3]
    # print(filtered_occur)
    fig, ax = plt.subplots()
    ax.bar(filtered_occur.index, filtered_occur["type_count"])
    ax.set_title(f"house type distribution")
    ax.tick_params("x", rotation=45, rotation_mode="xtick")
    plt.show()

def show_if_furnished(df):
    occur = df.groupby("furnished").size().to_frame("count")
    filtered_occur = occur[occur["count"] >= 3]
    # print(filtered_occur)
    fig, ax = plt.subplots()
    ax.bar(filtered_occur.index, filtered_occur["count"])
    ax.set_title(f"furnished/not-furnished")
    ax.tick_params("x", rotation=45, rotation_mode="xtick")
    plt.show()

# df = read_data()
# show_distribution(df, "price", 3)
# show_distribution(df, "surface", 3)
# show_distribution(df, "rooms", 3)
#
# show_city_distribution(df)
# show_house_type_distribution(df)
# show_if_furnished(df)
#
# box_price = df.boxplot(column="price")
# plt.show()
#
# box_surface = df["surface"].plot(kind="box", title="house area")
# plt.show()
