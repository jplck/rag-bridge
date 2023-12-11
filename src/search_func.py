import azure.functions as func
import logging
import os
from utils import get_vector_store
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
from sample_indexer import Sample_Indexer
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains.question_answering import load_qa_chain

http_search = func.Blueprint()
index_name = os.environ["COGNITIVE_SEARCH_INDEX_NAME"]

@http_search.route(route="search", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)

def search(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        prompt = req_body["prompt"]

        indexer = Sample_Indexer(index_name)

        search_result = search(indexer, prompt)
        
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
    
def search(indexer: Sample_Indexer, prompt: str) -> str:
    try:
        model = AzureChatOpenAI(
            openai_api_version="2023-05-15",
            azure_deployment=os.environ["OPENAI_DEPLOYMENT_NAME"],
        )

        result = indexer.search(prompt)

        template = """You are a chatbot having a conversation with a human. Provide a list of all found html links in your answer.
        {context}
        {history}
        Human: {input}
        Chatbot:"""

        prompt_template = PromptTemplate(
            input_variables=["history", "context", "input"], template=template
        )

        index_model = Sample_Indexer("test").get_model()
        vector_store = get_vector_store("memory", index_model)

        memory = VectorStoreRetrieverMemory(
            retriever=vector_store.as_retriever(),
            input_key="input",
        )

        chain = load_qa_chain(
            llm=model,
            prompt=prompt_template,
            verbose=True,
            memory=memory,
        )

        output = chain({ "input": prompt, "input_documents": result}, return_only_outputs=True)

        return output['output_text']
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return ""
