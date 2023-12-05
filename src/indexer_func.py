import os
import logging
import azure.functions as func
from langchain.embeddings import AzureOpenAIEmbeddings
from azure.search.documents.indexes import SearchIndexClient  
from langchain.vectorstores.azuresearch import AzureSearch
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from azure.search.documents.indexes.models import (
    ScoringProfile,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    TextWeights,
)
from utils import get_vector_store
import os
import json

idx = func.Blueprint()

embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(deployment=os.environ["OPENAI_EMBEDDINGS_DEPLOYMENT_NAME"], chunk_size=1)
index_name = os.environ["COGNITIVE_SEARCH_INDEX_NAME"]

@idx.schedule(schedule="5 * * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.') 

    create_index(index_name)
    fetch_documents("docs")

def fetch_documents(folder_path: str) -> None:
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    vector_store = get_vector_store(index_name)

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    data = json.load(file)
                    for doc in data:
                        content = doc["content"]
                        doc_id = doc["id"]
                        title = doc["title"]
                        documents = [content]
                        docs = text_splitter.split_documents(documents)
                        vector_store.add_documents(documents=docs, metadata={"source": filename, "id": doc_id, "title": title})

def create_index(index_name: str) -> None:
    embedding_function = embeddings.embed_query

    fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
            filterable=True,
        ),
        SearchableField(
            name="content",
            type=SearchFieldDataType.String,
            searchable=True,
        ),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=len(embedding_function("Text")),
            vector_search_configuration="default",
        ),
        SearchableField(
            name="metadata",
            type=SearchFieldDataType.String,
            searchable=True,
        ),
        # Additional field to store the title
        SearchableField(
            name="title",
            type=SearchFieldDataType.String,
            searchable=True,
        ),
        # Additional field for filtering on document source
        SimpleField(
            name="source",
            type=SearchFieldDataType.String,
            filterable=True,
        ),
    ]
    vector_store = get_vector_store(index_name)
    vector_store.fields.append(fields)