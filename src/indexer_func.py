import os
import logging
import azure.functions as func

from sample_indexer import Sample_Indexer
import os

idx = func.Blueprint()

index_name = os.environ["COGNITIVE_SEARCH_INDEX_NAME"]

@idx.schedule(schedule="15 * * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.') 

    indexer = Sample_Indexer(index_name)
    indexer.fetch(os.environ["DATA_ENPOINT_URL"])