import os
import pandas as pd  


def read_and_clean_data(name):
    link = "./data/raw/time_series_covid19_{}_global_narrow.csv".format(name)
    df = pd.read_csv(link, skiprows=[1], low_memory=False)
    df["Date"] = pd.to_datetime(df["Date"])
    df_final = df.sort_values("Date", ascending=True)
    df_final.columns = [
        "province",
        "country",
        "lat",
        "long",
        "date",
        "value_{}".format(name),
        "iso_code",
        "region_code",
        "subregion_code",
        "int_region-code"
    ]
    return df_final

def merge_dfs(list_of_dfs):
    df_main = list_of_dfs[0].copy()
    for df in list_of_dfs[1:]:
        df_main = pd.merge(df_main, df, how='outer', on=[
            "province",
            "country",
            "lat",
            "long",
            "date",
            "iso_code",
            "region_code",
            "subregion_code",
            "int_region-code",
        ])
    return df_main

def data_connect():
    df_con = read_and_clean_data("confirmed")
    df_dth = read_and_clean_data("deaths")
    df_rec = read_and_clean_data("recovered")

    df_merged = merge_dfs([df_con, df_dth, df_rec])
    
    df_grouped_country = df_merged.groupby(by=["country", "date"], as_index=False)[["value_deaths", "value_recovered", "value_confirmed"]].sum()
    
    df_world = df_grouped_country.groupby("date", as_index=False).sum()
    df_world["country"] = "World"
    
    df_main = df_grouped_country.append(df_world)
    return df_main