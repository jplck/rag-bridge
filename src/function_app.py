import azure.functions as func 
from indexer_func import idx
from search_func import http_search

app = func.FunctionApp() 

app.register_functions(idx)
app.register_functions(http_search)