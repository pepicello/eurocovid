""" Dash app """

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

data = pd.read_pickle("data/data.pkl")
latest = data["date"].max().strftime("%Y-%m-%d")
fig = pd.read_pickle("data/figure.pkl")[0]

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
    [dcc.Graph(figure=fig), html.Div(author, style={"padding-top": "5%"})]
)

if __name__ == "__main__":
    app.run_server(debug=False)
