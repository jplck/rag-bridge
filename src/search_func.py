import azure.functions as func
import logging
import os
from langchain.chat_models import AzureChatOpenAI
from sample_indexer import Sample_Indexer
from langchain.prompts import ChatPromptTemplate
from langchain.chains.question_answering import load_qa_chain

http_search = func.Blueprint()
index_name = os.environ["COGNITIVE_SEARCH_INDEX_NAME"]

@http_search.route(route="search", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)

def search(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        prompt = req_body["prompt"]
        history = req_body["history"]

        indexer = Sample_Indexer(index_name)

        search_result = search(indexer, prompt, history)
        
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
    
def search(indexer: Sample_Indexer, prompt: str, history: [str] = []) -> str:
    try:
        model = AzureChatOpenAI(
            openai_api_version="2023-05-15",
            azure_deployment=os.environ["OPENAI_DEPLOYMENT_NAME"],
        )

        search_results = indexer.search(prompt)

        chat_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a chatbot having a conversation with a human about energy topics. "
                           "You have received the following context to base your answer on: {context}. Also rely on the chat {history} if available. "
                           "Please wrap links you found in the context in html tags. """),
                ("human", "{user_input}"),
            ]
        )

        answer = model.invoke(chat_template.format_messages(
            context=search_results,
            history=history,
            user_input=prompt,
        ))

        return answer.content
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return ""
