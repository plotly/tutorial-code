from dash import Dash, dcc, html, callback, Output, Input, State
import dash_mantine_components as dmc  # pip install dash-mantine-components==0.12.0
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import find_dotenv, load_dotenv
import re
import os

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Create a .env file and write: OPENAI_API_KEY="insert-your-openai-token"

# Once you have your workspace, create your token by going to your databricks avatar -> settings -> developer -> Access tokens
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")  # Add to your ..env file: DATABRICKS_TOKEN="insert-your-token"
llm = ChatOpenAI(model_name="databricks-dbrx-instruct",  # this is the DBRX model
                 openai_api_key=DATABRICKS_TOKEN,
                 openai_api_base="https://dbc[...].databricks.com/serving-endpoints")
                 # the base_url will be sent to your email once your workspace is created. It's also in the 1st part of the url when you're in your workspace


prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)  # chain the LLM to the prompt

# Initialize the Dash app and define the layout
app = Dash()
app.layout = html.Div(
    [
        dmc.Container(  # dash-mantine-components==0.12.0
            children=[
                dmc.Title(order=1, children="Online Document Summarizer"),
                dmc.TextInput(label="Summarize Doc", placeholder="Enter the webpage or pdf...", id="input-1"),
                dmc.TextInput(label="Ask your question", placeholder="Ask away...", id="input-2"),
                dcc.Loading(html.Div(id='answer-space', children='')),
                dmc.Button(children="Submit", id="submit-btn", mt="md")
            ],
            style={"maxWidth": "500px", "margin": "0 auto"},
        )
    ]
)

@callback(
    Output('answer-space', 'children'),
    Input('submit-btn', 'n_clicks'),
    State('input-1', 'value'),
    State('input-2', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, input1, input2):
    if bool(re.search(r'\.pdf$', input1, re.IGNORECASE)):  # checks if link refers to a pdf
        # https://image-us.samsung.com/SamsungUS/tv-ci-resources/2018-user-manuals/2018_UserManual_Q9FNSeries.pdf
        loader = PyPDFLoader(input1)
        docs = loader.load_and_split()
    else:
        # load HTML pages and parse them
        # https://en.wikipedia.org/wiki/Paris
        loader = WebBaseLoader(input1)
        docs = loader.load()

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)
    vector = FAISS.from_documents(documents, embeddings)
    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    # Sample questions for testing app:
        # What was Paris architecture like in the 19th century
        # How can I fix my remote control?
    response = retrieval_chain.invoke(
        {"input": input2})

    return response["answer"]


if __name__ == '__main__':
    app.run_server(debug=False)
