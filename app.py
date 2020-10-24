""" Dash app """

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go

geometry = pd.read_pickle("data/geom.pkl").to_dict()
data = pd.read_pickle("data/data.pkl")
fig = go.Figure(
    go.Choroplethmapbox(
        geojson=geometry,
        locations=data["nuts_code"],
        z=data["rate_14_day_per_100k"],
        colorscale="Magma_r",
        marker_opacity=0.9,
        marker_line_width=0,
        text=data["region_name"]
        + " ("
        + data["country"]
        + "): "
        + data["date"].dt.strftime("%Y-%m-%d"),
    )
)
fig.update_layout(
    title_text="14-day COVID-19 case notification rate per 100 000",
    title_x=0.5,
    width=1000,
    height=700,
    mapbox=dict(center=dict(lat=54, lon=6.7), style="carto-positron", zoom=2.6),
)

# Dash app
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
    html.P(".", style={"display": "inline"}),
]
author = html.Div(auth_lst)
app = dash.Dash(__name__, title="Eurocovid", external_stylesheets=external_stylesheets)
app.layout = html.Div([dcc.Graph(figure=fig), author])

if __name__ == "__main__":
    app.run_server(debug=False)
