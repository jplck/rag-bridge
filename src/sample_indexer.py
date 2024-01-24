from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)
from langchain.embeddings import AzureOpenAIEmbeddings
import os
import json
from utils import add_to_index, get_vector_store
from langchain_core.documents import Document
from typing import List
import requests

class Sample_Indexer:

    _embeddings: AzureOpenAIEmbeddings
    _index_name: str

    def __init__(self, index_name: str) -> None:
        self._index_name = index_name
        self._embeddings = AzureOpenAIEmbeddings(deployment=os.environ["OPENAI_EMBEDDINGS_DEPLOYMENT_NAME"], chunk_size=1)

    def get_model(self) -> any:
        return [
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
                vector_search_dimensions=len(self._embeddings.embed_query("Text")),
                vector_search_configuration="default",
            ),
            SearchableField(
                name="title",
                type=SearchFieldDataType.String,
                searchable=True,
            ),
            SearchableField(
                name="metadata",
                type=SearchFieldDataType.String,
                searchable=True,
            ),
        ]
    
    def search(self, prompt: str) -> List[Document]:
        vector_store = get_vector_store(self._index_name, self.get_model())
        docs = vector_store.similarity_search(
            query=prompt,
            k=5,
            search_type="hybrid",
        )
        return docs

    def fetch(self, url: str) -> None:
        vector_store = get_vector_store(self._index_name, self.get_model())
        response = requests.post(url, json=None)
        if response.status_code == 200:
            data = response.json()
            for doc in data:
                content = doc["content"]
                title = doc["title"]
                doc_id = doc["id"]

                add_to_index(vector_store, content, title, doc_id)
        else:
            raise Exception(f"Failed to fetch JSON from endpoint. Status code: {response.status_code}")


    def fetch_local(self, folder_path: str) -> None:

        vector_store = get_vector_store(self._index_name, self.get_model())

        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for doc in data:
                            content = doc["content"]
                            title = doc["title"]
                            doc_id = doc["id"]

                            add_to_index(vector_store, content, title, doc_id)
    
