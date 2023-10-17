import micropip
await micropip.install('dash-bootstrap-components')
from dash import Dash, html, dcc, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

# App layout
app.layout = dbc.Container([
    html.H1(children='Country Analysis'),
    html.Hr(),
    
    dbc.Row([
        dbc.Col([
            dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='yaxis-options'),   
        ], width=6),
        dbc.Col([
            dcc.Dropdown(options=['country', 'continent'], value='continent', id='xaxis-options'),    
        ], width=6)
    ], className='mb-3'),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure={}, id='graph1')
        ], width=12)
    ]),
])

# Add controls to build the interaction
@callback(
    Output(component_id='graph1', component_property='figure'),
    Input(component_id='yaxis-options', component_property='value'),
    Input(component_id='xaxis-options', component_property='value'),
    
)
def update_graph(y_chosen, x_chosen):
    fig = px.histogram(df, x=x_chosen, y=y_chosen, histfunc='avg')
    return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
