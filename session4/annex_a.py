import micropip
await micropip.install('dash-bootstrap-components')
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = dbc.Container([
        dbc.Row(
            [
                dbc.Col(dbc.Alert("One of three columns"), md=4),
                dbc.Col(dbc.Alert("One of three columns"), md=4),
                dbc.Col(dbc.Alert("One of three columns"), md=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Alert("One of four columns"), width=6, lg=3),
                dbc.Col(dbc.Alert("One of four columns"), width=6, lg=3),
                dbc.Col(dbc.Alert("One of four columns"), width=6, lg=3),
                dbc.Col(dbc.Alert("One of four columns"), width=6, lg=3),
            ]
        )
])



if __name__ == "__main__":
    app.run_server()
