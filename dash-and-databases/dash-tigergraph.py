# Import libraries ----------------------------------------------------------------------------------------------------
from dash import Dash, html, dcc, Output, Input, callback  # pip install dash
import plotly.express as px
import pandas as pd             # pip install pandas
import pyTigerGraph as tg       # pip install pyTigerGraph

# Connect to TigerGraph data ------------------------------------------------------------------------------------------
TG_HOST = 'https://plotly-relationship.i.tgcloud.io/'
TG_USERNAME = 'tigergraph'
TG_PASSWORD = 'tigergraph'
TG_GRAPHNAME = 'connectivity'

conn = tg.TigerGraphConnection(host=TG_HOST, username=TG_USERNAME, password=TG_PASSWORD)
authToken = conn.getToken('aa12gam70lud3gaeffhnfueokpaiuejb')[0]
conn = tg.TigerGraphConnection(host=TG_HOST, username=TG_USERNAME,
                               password=TG_PASSWORD, graphname=TG_GRAPHNAME,
                               apiToken=authToken)

# Run Installed Query:
our_data = conn.runInstalledQuery('get_calls_by_person')
df = conn.vertexSetToDataFrame(our_data[0]['res'])
df['dob'] = pd.to_datetime(df['dob'], unit='ms')
print(df.columns.values)

# Define app layout ---------------------------------------------------------------------------------------------------
app = Dash(__name__)

my_dropdown = dcc.Dropdown(options=['gender', 'ethnic_group', 'num_phones'],
                           value='gender',
                           multi=False,
                           style={'width': '50%'})
num_calls_graph = dcc.Graph(figure={})

app.layout = html.Div([
    html.H1('Connect TigerGraph to Plotly and Dash', style={'textAlign': 'center'}),
    # html.Label("Select dataset size:"),
    # data_size := dcc.RadioItems(options=[100, 500, 1000], value=500),
    html.Label("Select X-axis:"),
    my_dropdown,
    num_calls_graph
])

# Connect layout components (graphs to dropdown value) ----------------------------------------------------------------
@callback(
    Output(component_id=num_calls_graph, component_property='figure'),
    Input(component_id=my_dropdown, component_property='value'),
    # Input(component_id=data_size, component_property='value'),
)
def update_graph(dropdown_value):
    print(dropdown_value)
    # Run an Installed Query: -----------------------------------------------------------------------------------------
    num_calls_figure = px.bar(data_frame=df, x=dropdown_value, y='num_calls')
    return num_calls_figure

    # Run an Interpreted Query: ---------------------------------------------------------------------------------------
#     our_data = conn.runInterpretedQuery("""
#     Interpret QUERY get_calls_by_person_limited(int datasize) FOR GRAPH connectivity SYNTAX v2{
#       people = {Person.*};
#       accounts = {BankAccount.*};
#       SumAccum<FLOAT> @tot_duration;
#       SumAccum<INT> @num_calls;
#       BagAccum<VERTEX<Phone>> @phones;
#       SumAccum<INT> @num_phones;
#
#   res = SELECT p FROM people:p - () - Phone:b - () - PhoneCall:f
#     ACCUM
#       p.@tot_duration += f.callLength,
#       p.@num_calls += 1,
#       p.@phones += b
#     POST-ACCUM
#       p.@num_phones += p.@phones.size()
#     LIMIT datasize;
#
#   PRINT res [res.gender AS gender, res.dob AS dob, res.ethic_group AS ethnic_group, res.@tot_duration AS tot_duration, res.@num_calls AS num_calls, res.@num_phones AS num_phones];
# }
#     """, params={'datasize':d_size})
#     df = conn.vertexSetToDataFrame(our_data[0]['res'])
#     df['dob'] = pd.to_datetime(df['dob'], unit='ms')
#     num_calls_figure = px.bar(data_frame=df, x=dropdown_value, y='num_calls')
#     return num_calls_figure


if __name__ == '__main__':
    app.run_server(debug=True)
