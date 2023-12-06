import os
import logging
import azure.functions as func

from utils import create_index
from model import file_based_sample_model
from data_interfaces import fetch_documents
import os

idx = func.Blueprint()

index_name = os.environ["COGNITIVE_SEARCH_INDEX_NAME"]

@idx.schedule(schedule="15 * * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.') 

    create_index(index_name, file_based_sample_model)
    fetch_documents("docs")