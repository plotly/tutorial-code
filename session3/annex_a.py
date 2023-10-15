import micropip
await micropip.install("dash_ag_grid")

from dash import Dash, html, dcc, Input, Output, callback, no_update
import dash_ag_grid as dag
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

columnDefs = [
    { 'field': 'country' },
    { 'field': 'pop' },
    { 'field': 'continent'},
    { 'field': 'lifeExp' },
    { 'field': 'gdpPercap' }
]

grid = dag.AgGrid(
    id="tabular-data",
    rowData=df.to_dict("records"),
    columnDefs=columnDefs,
)

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data, Graph, and Controls'),
    html.Hr(),
    dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='radio-buton'),
    grid,
    dcc.Graph(figure={}, id='my-histogram')
])

# Add controls to build the interaction
@callback(
    Output(component_id='my-histogram', component_property='figure'),
    Input(component_id='radio-buton', component_property='value')
)
def update_graph(yaxis_chosen):
    fig = px.histogram(df, x='continent', y=yaxis_chosen, histfunc='avg')
    return fig
