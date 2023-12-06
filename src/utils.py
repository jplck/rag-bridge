import os
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.vectorstores.azuresearch import AzureSearch
from langchain.text_splitter import CharacterTextSplitter

def get_vector_store(for_index: str, fields: any) -> AzureSearch:
    embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(deployment=os.environ["OPENAI_EMBEDDINGS_DEPLOYMENT_NAME"], chunk_size=1)
    return AzureSearch(
        azure_search_endpoint=os.environ["COGNITIVE_SEARCH_ENDPOINT"],
        azure_search_key=os.environ["COGNITIVE_SEARCH_KEY"],
        index_name=for_index,
        embedding_function=embeddings.embed_query,
        fields=fields,
    )

def add_to_index(vector_store: AzureSearch, text: str, title: str, doc_id: str) -> None:
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=0)
    chunks = text_splitter.split_text(text)
                        
    for i, chunk in enumerate(chunks):
        vector_store.add_texts(
            keys=[f"{doc_id}_{i}"],
            texts=[chunk],
            metadatas=[{"source": "docs", "title": title}],
    )