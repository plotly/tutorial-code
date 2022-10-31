from datetime import date, datetime

import dash
from dash import Dash, Input, Output, dcc, html, callback
import plotly.express as px
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2016-weather-data-seattle.csv")

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Historic Weather Data in Seattle", style={'textAlign': 'center'}),
    dcc.DatePickerSingle(
        id='my-date-picker',
        min_date_allowed=date(1948, 1, 1),
        max_date_allowed=date(2015, 12, 31),
        initial_visible_month=date(1948, 1, 1),
        date=date(1948, 1, 1)
    ),
    dcc.Graph(figure={}, id='my-graph'),
])

@callback(
    Output('my-graph', 'figure'),
    Input('my-date-picker', 'date')
)
def update_graph(date_value):
    if date_value:
        date_value = datetime.strptime(date_value, '%Y-%m-%d').strftime('%#m/%#d/%Y')
        dff = df[df['Date'] == date_value]
        my_bar = px.bar(dff,
                        y=['Max_TemperatureC','Mean_TemperatureC','Min_TemperatureC'],
                        barmode='group',
        )
        my_bar.update_traces(hovertemplate='<br>%{y} C')
        my_bar.update_layout(xaxis_visible= False)
        return my_bar
    else:
        dash.no_update()


if __name__ == '__main__':
    app.run_server(debug=True)