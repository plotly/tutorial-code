from dash import Dash, html, dcc, callback, Input, Output, State
app = Dash(__name__)

app.layout = html.Div([
    html.H1('Dash Training Room', style={'textAlign':'center'}),
    dcc.Markdown("""
        ```
        from dash import Dash, html
        
        app = Dash(__name__)
        
        app.layout = html.Div([
            html.Div(children="hello world")
        ])
        
        if __name__ == '__main__':
            app.run_server()
        ```
        
        What is the output of this code?
    """),
    dcc.Input(id='user-input'),
    html.Button('Submit', id='btn'),
    html.Hr(style={'borderBottom': '2px solid'}),
    html.Div(id='user-output')
])


@callback(
    Output('user-output', 'children'),
    Input('btn', 'n_clicks'),
    State('user-input', 'value'),
prevent_initial_call=True
)
def solution(n, value):
    if value == 'hello world':
        return dcc.Markdown("""
            Way to go! That is correct.
            
            Solution:
            
            hello world
            
            Why?
            
            The string assigned to the children of an html.Div represents what is displayed on the page.
            Just make sure that the Div is inside the app layout.
            """
        )
    else:
        return dcc.Markdown("""
            Nice Try. Let's try another puzzle.

            Solution:
            
            hello world

            Why?

            The string assigned to the children of an html.Div represents what is displayed on the page.
            Just make sure that the Div is inside the app layout.
            """
        )


if __name__ == '__main__':
    app.run_server()
