import os
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.vectorstores.azuresearch import AzureSearch

def get_vector_store(for_index: str) -> AzureSearch:
    embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(deployment=os.environ["OPENAI_EMBEDDINGS_DEPLOYMENT_NAME"], chunk_size=1)
    return AzureSearch(
        azure_search_endpoint=os.environ["COGNITIVE_SEARCH_ENDPOINT"],
        azure_search_key=os.environ["COGNITIVE_SEARCH_KEY"],
        index_name=for_index,
        embedding_function=embeddings.embed_query,
    )