""" Retrieve and process data """

from pathlib import Path

import geojson
import pandas as pd
import requests
import tqdm
import yaml
from loguru import logger

daily = "https://opendata.ecdc.europa.eu/covid19/subnationalcasedaily/csv"
weekly = "https://opendata.ecdc.europa.eu/covid19/subnationalcaseweekly/csv"
data_links = {"daily": daily, "weekly": weekly}
logger.add("logs/main.txt")

if __name__ == "__main__":

    # Retrieve
    for freq, link in data_links.items():
        csv_file = requests.get(link, allow_redirects=True)
        with open(f"data/{freq}.csv", "wb") as f:
            f.write(csv_file.content)
    logger.info("Data retrieved from ECDC")

    # Process
    files = {"daily": Path("./data/daily.csv"), "weekly": Path("./data/weekly.csv")}
    data = pd.DataFrame()
    for freq, file in files.items():
        df = pd.read_csv(file)
        if freq == "weekly":
            # Updated every Wed
            fmt = "%Y-W%W-%w"
            add_day = df.year_week.apply(lambda x: str(x) + "-3")
            df["date"] = pd.to_datetime(add_day, format=fmt)
            df.drop("year_week", axis=1, inplace=True)
        elif freq == "daily":
            df["date"] = pd.to_datetime(df.date)
        data = data.append(df)

    # Manual fixes
    with open("configs/nuts_mapping.yml", "r") as f:
        nuts_mapping = yaml.load(f)
    nuts_dict = {f"^{k}$": v for k, v in nuts_mapping["mapping"].items()}
    data["nuts_code"] = data["nuts_code"].astype(str).replace(nuts_dict, regex=True)
    data = data.loc[~data.nuts_code.isin(nuts_mapping["delete"])]
    data = data.dropna(subset=["rate_14_day_per_100k"])
    data["rate_14_day_per_100k"] = data["rate_14_day_per_100k"].round()

    # geoJson for nuts codes (EU)
    geometry = {}
    for level in [0, 1, 2, 3]:
        with open(
            f"data/ref-nuts-2016-10m.geojson/NUTS_RG_10M_2016_4326_LEVL_{level}.geojson",
            "r",
            encoding="utf-8",
        ) as f:
            geom_file = geojson.load(f)
            geometry["type"] = geom_file["type"]
            geometry["crs"] = geom_file["crs"]
            if "features" in geometry:
                geometry["features"].extend(geom_file["features"])
            else:
                geometry["features"] = geom_file["features"]

    # Select only usefule geom features
    present_nuts = []
    nuts_list = data["nuts_code"].tolist()
    for feature in geometry["features"]:
        if feature["id"] in nuts_list:
            present_nuts.append(feature)
    geometry["features"] = present_nuts

    # Check that there are no mismatched NUTS
    geojsondf = (
        pd.Series(geometry["features"])
        .apply(lambda x: pd.Series(x))
        .rename(columns=dict(id="nuts_code"))[["nuts_code", "geometry"]]
    )
    data_with_geom = pd.merge(data, geojsondf, on="nuts_code", how="outer")

    if not data_with_geom.loc[lambda x: x.geometry.isna()].empty:
        logger.error("Mismatch is NUTS, please check data")
        raise ValueError("Mismatch is NUTS, please check data")

    # Fill missing data and restrict to weekly
    dates_in_data = set(data_with_geom["date"].tolist())
    date_list = pd.date_range(
        data_with_geom["date"].min(), data_with_geom["date"].max(), freq="W-WED"
    ).tolist()
    date_list = [x for x in date_list if x in dates_in_data]
    output = pd.DataFrame()
    for date in tqdm.tqdm(date_list, desc="Date"):
        pit_data = data_with_geom.loc[data_with_geom["date"] <= date]
        cur_data = pit_data.groupby("nuts_code").apply(
            lambda x: x.sort_values("date").iloc[-1]
        )
        cur_data["current_date"] = date
        output = output.append(cur_data)
    output = output.reset_index(drop=True)

    # Save processed data
    pd.Series(geometry).to_pickle("data/geom.pkl")
    output.to_pickle("data/data.pkl")
    logger.info("Data processed and saved!")
