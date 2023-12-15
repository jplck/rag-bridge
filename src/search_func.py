import azure.functions as func
import logging
import os
from langchain.chat_models import AzureChatOpenAI
from sample_indexer import Sample_Indexer
from langchain.prompts import ChatPromptTemplate
from langchain.chains.openai_functions import (
    create_openai_fn_chain,
    create_openai_fn_runnable,
    create_structured_output_chain,
    create_structured_output_runnable,
)
from langchain_core.documents import Document
from typing import List

http_search = func.Blueprint()
index_name = os.environ["COGNITIVE_SEARCH_INDEX_NAME"]
_indexer: Sample_Indexer

@http_search.route(route="search", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def search(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        prompt = req_body["prompt"]

        _indexer = Sample_Indexer(index_name)

        search_result = search(prompt)
        
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

def search(prompt: str) -> str:
    """Search trough a database of faqs, related to wallbox topics.

    Args:
        prompt: Thhe prompt to search for.
    """
    return _indexer.search(prompt).to_json()

def search(prompt: str) -> str:
    try:
        model = AzureChatOpenAI(
            openai_api_version="2023-05-15",
            azure_deployment=os.environ["OPENAI_DEPLOYMENT_NAME"],
        )

        #search_results = indexer.search(prompt)

        chat_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a chatbot having a conversation with a human about energy topics. "
                           "Please wrap links you found in the context in html tags. """),
                ("human", "{user_input}"),
            ]
        )

        runnable = create_openai_fn_runnable([search], model, chat_template)
        answer = runnable.invoke({"user_input": prompt})

        return answer.content
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return ""
