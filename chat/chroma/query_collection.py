from chat.chroma.chroma_interface import ChromaInterface
import json

if __name__ == "__main__":

    collection_name = "roko-telegram"
    query = "How will the roko network be driven?"
    n_results = 3

    ci = ChromaInterface()
    print(f"Collection has {ci.count_collection(collection_name):,} documents.")
    results = ci.query(collection_name, query, n_results)
    print(json.dumps(results, indent=2))
