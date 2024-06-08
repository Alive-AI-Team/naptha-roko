import chromadb

CHROMA_HOST = "localhost"
CHROMA_PORT = 8000
CHROMA_COLLECTION = "roko-telegram"
QUERY = "How will the roko network be driven?"
NUM_RESULTS = 3

if __name__ == "__main__":

    # ensure chroma is running: i.e. chroma run --path ./chroma.db
    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    
    collection = client.get_collection(name=CHROMA_COLLECTION)
    print(f"Collection {CHROMA_COLLECTION} has {collection.count():,} entries.")

    print(f"Query is: {QUERY}")

    result = collection.query(query_texts=[QUERY], n_results=NUM_RESULTS)
    print(result)