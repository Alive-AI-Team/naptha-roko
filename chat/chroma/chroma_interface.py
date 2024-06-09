import chromadb
import json
from pathlib import Path
from tqdm import tqdm


class ChromaDataGenerator:
    """Just a placeholder to indicate that different types of
    generators can exist and so we can use it in type hints.
    All generators should have get_messages and return the
    text, meta, id fields
    """

    pass


class TelegramJsonGenerator(ChromaDataGenerator):

    def __init__(self, json_path: str | Path, min_message_len=100):
        self.min_message_len = min_message_len
        with open(json_path, "r") as fp:
            data = json.load(fp)
            self.messages = data.get("messages", [])

    def get_messages(self):
        for message in self.messages:
            if len(str(message.get("text", ""))) >= self.min_message_len:
                yield {
                    "text": str(message.get("text", "")),
                    "meta": {
                        "date": str(message.get("date", "")),
                        "from_id": str(message.get("from_id", "")),
                    },
                    "id": str(message["id"]),
                }


class ChromaInterface:

    def __init__(self, host="localhost", port=8000):
        self.client = chromadb.HttpClient(host=host, port=port)

    def create_collection(self, name: str, data_src: ChromaDataGenerator):

        collection = self.client.create_collection(name=name)
        for message in tqdm(data_src.get_messages()):
            collection.add(
                documents=[message["text"]], metadatas=[message["meta"]], ids=[message["id"]]
            )

    def count_collection(self, collection_name: str) -> int:
        collection = self.client.get_or_create_collection(collection_name)
        return collection.count()

    def query(
        self, collection_name: str, query_text: str, n_results: int
    ) -> chromadb.QueryResult:
        collection = self.client.get_or_create_collection(collection_name)
        return collection.query(query_texts=[query_text], n_results=n_results)

