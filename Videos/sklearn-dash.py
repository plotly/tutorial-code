from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_ag_grid as dag
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


wine = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/winequality-red.csv')
quality_label = LabelEncoder()
wine['quality'] = quality_label.fit_transform(wine['quality'])
X = wine.drop('quality', axis = 1)
y = wine['quality']
print(wine.columns)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container(
    [
        html.H1('Scikit-Learn with Dash', style={'textAlign': 'center'}),
        dbc.Row([
            dbc.Col([
                html.Div("Select Test Size:"),
                dcc.Input(value=0.2, type='number', debounce=True, id='test-size', min=0.1, max=0.9, step=0.1)
            ], width=3),
            dbc.Col([
                html.Div("Select RandomForest n_estimators:"),
                dcc.Input(value=150, type='number', debounce=True, id='nestimator-size', min=10, max=200, step=1)
            ], width=3),
            dbc.Col([
                html.Div("Accuracy Score:"),
                html.Div(id='placeholder', style={'color':'blue'}, children="")
            ], width=3)
        ], className='mb-3'),

        dag.AgGrid(
            id="grid",
            rowData=wine.to_dict("records"),
            columnDefs=[{"field": i} for i in wine.columns],
            columnSize="sizeToFit",
            style={"height": "310px"},
            dashGridOptions={"pagination": True, "paginationPageSize":5},
        ),

        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=px.histogram(wine, 'fixed acidity', histfunc='avg')),
            ], width=6),
            dbc.Col([
                dcc.Graph(figure=px.histogram(wine, 'pH', histfunc='avg')),
            ], width=6)
        ]),
    ]
)


@callback(
    Output('placeholder', 'children'),
    Input('test-size', 'value'),
    Input('nestimator-size', 'value')
)
def update_testing(test_size_value, nestimator_value):
    # Train and Test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size_value, random_state=2)

    # Apply Standard scaling
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.fit_transform(X_test)

    # Random Forest Classifier
    rfc = RandomForestClassifier(n_estimators=nestimator_value)
    rfc.fit(X_train, y_train)
    pred_rfc = rfc.predict(X_test)
    score = accuracy_score(y_test, pred_rfc)

    return score


if __name__=='__main__':
    app.run_server()
