from dash import Dash, html, dcc, callback, Output, Input, no_update
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
import os

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
# Once you have your databricks workspace, create your token by going to your databricks avatar -> settings -> developer -> Access tokens
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")  # Create a .env file and write: DATABRICKS_TOKEN="insert-your-token"

client = OpenAI(
    api_key=DATABRICKS_TOKEN,
    base_url="https://dbc-[...].databricks.com/serving-endpoints"
    # the base_url will be sent to your email once your workspace is created. It's also in the 1st part of the url when you're in your workspace
)

app = Dash()
app.layout = [
    dcc.Markdown("# Minimal example of a Chat Dash app"),
    html.Label("Type your question to activate the DBRX LLM"),
    html.P(),
    dcc.Input(id='user-input', type='text', debounce=True),  # debounce will delay the Input Processing until after you hit Enter
    html.Div(id='response-space', children=response)
]


@callback(
    Output('response-space', 'children'),
    Input('user-input', 'value'),
    prevent_initial_call=True
)
def activate_chat(input_value):
    if not input_value:  # don't update the output if the input value is empty (no text)
        return no_update
    else:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant"
                },
                {
                    "role": "user",
                    "content": input_value
                }
            ],
            model="databricks-dbrx-instruct",  # this is the DBRX model
            max_tokens=256
        )
        print(chat_completion)
        response = chat_completion.choices[0].message.content
        return response



if __name__ == '__main__':
    app.run_server(debug=False, port=8008)
