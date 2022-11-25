from dash import Dash, Input, Output, dcc, html, callback
import plotly.express as px
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2016-weather-data-seattle.csv")
df = df[df['Max_TemperatureC']<54] # remove row with an error in temperature. Seattle never experienced 54 degrees


app = Dash(__name__)

app.layout = html.Div([
    html.H1("Number of days within high temperature range", style={'textAlign': 'center'}),
    dcc.RangeSlider(
        min=df['Min_TemperatureC'].min(),
        max=df['Max_TemperatureC'].max(),
        step=1,
        value=[30, 35],
        tooltip={"placement": "bottom", "always_visible": True},
        id='my-range',
        marks={
            int(df['Min_TemperatureC'].min()):{'label': str(df['Min_TemperatureC'].min()), 'style': {'color': 'blue'}},
            -10: {'label': '-10°C'},
            0: {'label': '0°C'},
            10: {'label': '10°C'},
            20: {'label': '20°C'},
            30: {'label': '30°C'},
            int(df['Max_TemperatureC'].max()): {'label': str(df['Max_TemperatureC'].max()), 'style': {'color': '#FF0000'}}
    }
    ),
    dcc.Graph(figure={}, id='my-graph'),
])

@callback(
    Output('my-graph', 'figure'),
    Input('my-range', 'value')
)
def update_graph(temp_list):
    dff = df[(df['Max_TemperatureC']>=temp_list[0]) & (df['Max_TemperatureC']<=temp_list[1])]
    print(dff.head())
    fig = px.histogram(dff, x='Max_TemperatureC', labels={'Max_TemperatureC': 'Daily High'})
    return fig


if __name__ == '__main__':
    app.run()
