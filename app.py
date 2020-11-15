""" Dash app """

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

geometry = pd.read_pickle("data/geom.pkl").to_dict()
data = pd.read_pickle("data/data.pkl")
curr_data = pd.read_pickle("data/curr_data.pkl")
latest = data["date"].max().strftime("%Y-%m-%d")
date_dict = (
    data["date"]
    .drop_duplicates()
    .dropna()
    .sort_values()
    .reset_index(drop=True)
    .to_dict()
)
last_date_idx = max(list(date_dict.keys()))
max_z = round(data["rate_14_day_per_100k"].max(), -3)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
auth_lst = [
    html.P("Created by ", style={"display": "inline"}),
    html.A("Giulio Pepe", href="http://giuliopepe.com", style={"display": "inline"}),
    html.P(". Data from ", style={"display": "inline"}),
    html.A("ECDC", href="https://www.ecdc.europa.eu", style={"display": "inline"}),
    html.P(". More info ", style={"display": "inline"}),
    html.A(
        "here",
        href="https://github.com/pepicello/eurocovid",
        style={"display": "inline"},
    ),
    html.P(f". Latest update: {latest}", style={"display": "inline"}),
]
author = html.Div(auth_lst)
app = dash.Dash(__name__, title="Eurocovid", external_stylesheets=external_stylesheets)
app.layout = html.Div(
    [
        dcc.Graph(id="map"),
        html.Div(id="update_slider_text", style={"padding-left": "5%"}),
        html.Div(
            dcc.Slider(
                id="time_slider", min=0, max=last_date_idx, step=1, value=last_date_idx,
            ),
            style={"width": "50%", "padding-left": "5%"},
        ),
        html.Div(author, style={"padding-top": "2%", "padding-left": "5%"}),
    ]
)


@app.callback(Output("update_slider_text", "children"), [Input("time_slider", "value")])
def display_value(time_idx):
    return "Change date: {}".format(date_dict[time_idx].strftime("%Y-%m-%d"))


@app.callback(Output("map", "figure"), [Input("time_slider", "value")])
def map_gen(time_idx):
    if time_idx == last_date_idx:
        plot_data = curr_data
    else:
        plot_data = data.loc[data["date"] <= date_dict[time_idx]]
        plot_data = (
            plot_data.groupby("nuts_code")
            .apply(lambda x: x.sort_values("date").iloc[-1])
            .reset_index(drop=True)
        )
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=geometry,
            locations=plot_data["nuts_code"],
            z=plot_data["rate_14_day_per_100k"],
            colorscale="Magma_r",
            marker_opacity=0.9,
            marker_line_width=0,
            zmin=0,
            zmax=max_z,
            text=plot_data["region_name"]
            + " ("
            + plot_data["country"]
            + "): "
            + plot_data["date"].dt.strftime("%Y-%m-%d"),
        )
    )
    fig.update_layout(
        title_text="14-day COVID-19 case notification rate per 100 000",
        title_x=0.5,
        width=1000,
        height=700,
        uirevision=True,
        mapbox=dict(center=dict(lat=54, lon=6.7), style="carto-positron", zoom=2.6),
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=False)
