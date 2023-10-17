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
    dbc.Alert(id='app-alert', is_open=False, duration=3000, children='Try a different combination please!'),
    
    dbc.Row([
        dbc.Col([
            dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='yaxis-options'),   
        ], width=6),
        dbc.Col([
            dcc.Dropdown(options=['country', 'continent'], value='continent', id='xaxis-options'),  
            dbc.Button('Submit', id='my-button', n_clicks=0)
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
    Output(component_id='app-alert', component_property='is_open'),
    Input(component_id='my-button', component_property='n_clicks'),
    State(component_id='yaxis-options', component_property='value'),
    State(component_id='xaxis-options', component_property='value'),
    
)
def update_graph(_, y_chosen, x_chosen):
    if y_chosen=='pop' and x_chosen=='country':
        return no_update, True
    else:
        fig = px.histogram(df, x=x_chosen, y=y_chosen, histfunc='avg')
        return fig, no_update


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
