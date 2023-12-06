import os
import json
from utils import add_to_index

def fetch_documents(folder_path: str) -> None:
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

                        add_to_index("docs", content, title, doc_id)

                        