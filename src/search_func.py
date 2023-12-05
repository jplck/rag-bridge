import azure.functions as func
import logging
import os
from utils import get_vector_store
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
import json

http_search = func.Blueprint()
index_name = os.environ["COGNITIVE_SEARCH_INDEX_NAME"]

@http_search.route(route="search", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)

def search(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        prompt = req_body["prompt"]
        search_result = search(index_name, prompt)
        
        if prompt:
            return func.HttpResponse(search_result)
        else:
            return func.HttpResponse(
                 "Please enter a prompt to search for.",
                 status_code=401
            )
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON format.",
            status_code=400
        )
    
def search(index_name: str, prompt: str) -> str:
    model = AzureChatOpenAI(
        openai_api_version="2023-05-15",
        azure_deployment=os.environ["OPENAI_DEPLOYMENT_NAME"],
    )
    vector_store = get_vector_store(index_name)
    docs = vector_store.similarity_search(
        query=prompt,
        k=3,
        search_type="hybrid",
    )
    
    result = docs[0].page_content

    message = HumanMessage(
        content=f"Take the search results from {result} and use them to generate a response to the prompt {prompt}.",
    )
    return model([message]).content
