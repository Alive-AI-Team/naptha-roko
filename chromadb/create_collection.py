import chromadb
import json
from pathlib import Path

CHROMA_PATH = "./chroma.db"
CHROMA_COLLECTION = "roko-telegram"
JSON_FNAME = "/home/julien/data/naptha/roko-telegram-export.json"
MIN_MESSAGE_LEN = 80

if __name__ == "__main__":

    assert(not Path(CHROMA_PATH).is_dir())

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    print(f"Created DB: {CHROMA_PATH}")
    collection = client.create_collection(name=CHROMA_COLLECTION)

    with open(JSON_FNAME, "r") as fp:
        dat = json.load(fp)
        assert("messages" in dat.keys())
        print(f"We have {len(dat['messages'])} messages")

        for message in dat["messages"]:
            if len(message["text"]) > MIN_MESSAGE_LEN:
                print(f"Inserting message {message['id']}")
                text = str(message["text"])
                meta = { 
                    "date": message["date"],
                    "from_id": message["from_id"]
                }
                id = str(message["id"])
                print(text)
                print(meta)
                print(id)
                collection.add(documents=[text], metadatas=[meta], ids=[id])

        print(f"Collection now has: {collection.count()} entries.")