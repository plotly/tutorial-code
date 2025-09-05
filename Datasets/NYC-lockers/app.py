# check out https://dash.plotly.com/ for documentation
from dash import Dash, Input, Output, callback, dcc, html
import plotly.express as px
import pandas as pd

# https://raw.githubusercontent.com/plotly/tutorial-code/refs/heads/main/Datasets/lockerNYC.csv
df = pd.read_csv("lockerNYC.csv")

fig = px.histogram(df, x='Locker Size')

app = Dash(__name__)
app.layout = html.Div(
    children=[
        dcc.Graph(figure=fig)
    ]
)


if __name__ == '__main__':
    app.run(debug=True)
