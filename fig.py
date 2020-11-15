""" Create figure object """

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sel_col = [
    "date",
    "current_date",
    "nuts_code",
    "rate_14_day_per_100k",
    "region_name",
    "country",
]
rename_cols = dict(rate_14_day_per_100k="Rate", region_name="Region", country="Country")

geometry = pd.read_pickle("data/geom.pkl").to_dict()
data = pd.read_pickle("data/data.pkl")
data = data[sel_col]
data["Update Date"] = data["date"].dt.strftime("%Y-%m-%d")
data["Current Date"] = data["current_date"].dt.strftime("%Y-%m-%d")
data = data.rename(columns=rename_cols)
data = data.sort_values("current_date")
max_z = round(data["Rate"].max(), -3)

fig = px.choropleth_mapbox(
    data,
    geojson=geometry,
    locations="nuts_code",
    color="Rate",
    color_continuous_scale="Magma_r",
    range_color=(0, max_z),
    mapbox_style="carto-positron",
    opacity=0.9,
    center={"lat": 54, "lon": 6.7},
    title="<b>14-day COVID-19 case notification rate per 100 000</b>",
    zoom=2.4,
    hover_name="Region",
    hover_data={
        "Current Date": False,
        "nuts_code": False,
        "Rate": True,
        "Country": True,
        "Update Date": True,
    },
    animation_frame="Current Date",
    width=1000,
    height=700,
)

fig.layout["sliders"][0]["active"] = len(fig.frames) - 1
fig = go.Figure(data=fig["frames"][-1]["data"], frames=fig["frames"], layout=fig.layout)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_traces(marker_line_width=0)

pd.Series({0: fig}).to_pickle("data/figure.pkl")
