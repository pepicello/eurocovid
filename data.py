""" Retrieve and process data """

from pathlib import Path

import geojson
import pandas as pd
import requests
import yaml
from loguru import logger

daily = "https://opendata.ecdc.europa.eu/covid19/subnationalcasedaily/xlsx"
weekly = "https://opendata.ecdc.europa.eu/covid19/subnationalcaseweekly/xlsx"
data_links = {"daily": daily, "weekly": weekly}
logger.add("logs/main.txt")

if __name__ == "__main__":

    # Retrieve
    for freq, link in data_links.items():
        xlsx = requests.get(link, allow_redirects=True)
        with open(f"data/{freq}.xlsx", "wb") as f:
            f.write(xlsx.content)
    logger.info("Data retrieved from ECDC")

    # Process
    files = {"daily": Path("./data/daily.xlsx"), "weekly": Path("./data/weekly.xlsx")}
    all_data = pd.DataFrame()
    for freq, file in files.items():
        df = pd.read_excel(file)
        if freq == "weekly":
            # Updated every Wed
            fmt = "%Y-W%W-%w"
            add_day = df.year_week.apply(lambda x: str(x) + "-3")
            df["date"] = pd.to_datetime(add_day, format=fmt)
            df.drop("year_week", axis=1, inplace=True)
        elif freq == "daily":
            df["date"] = pd.to_datetime(df.date)
        all_data = all_data.append(df)

    # Gets most recent figure
    data = (
        all_data.groupby("nuts_code")
        .apply(lambda x: x.sort_values("date").iloc[-1])
        .reset_index(drop=True)
    )

    # Manual fixes
    with open("configs/nuts_mapping.yml", "r") as f:
        nuts_mapping = yaml.load(f)
    nuts_dict = {f"^{k}$": v for k, v in nuts_mapping["mapping"].items()}
    data["nuts_code"] = data["nuts_code"].astype(str).replace(nuts_dict, regex=True)
    data = data.loc[~data.nuts_code.isin(nuts_mapping["delete"])]

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

    geojsondf = (
        pd.Series(geometry["features"])
        .apply(lambda x: pd.Series(x))
        .rename(columns=dict(id="nuts_code"))[["nuts_code", "geometry"]]
    )
    data_with_geom = pd.merge(data, geojsondf, on="nuts_code", how="outer")

    # No mismatched NUTS
    if not data_with_geom.loc[lambda x: x.geometry.isna()].empty:
        logger.error("Mismatch is NUTS, please check data")
        raise ValueError("Mismatch is NUTS, please check data")

    # Save processed data
    pd.Series(geometry).to_pickle("data/geom.pkl")
    data_with_geom.to_pickle("data/data.pkl")
    logger.info("Data processed and saved!")
