from chat.chroma.chroma_interface import ChromaInterface, TelegramJsonGenerator

if __name__ == "__main__":

    json_path = "/home/julien/data/naptha/roko-telegram-export.json"
    collection_name = "roko-telegram"

    ci = ChromaInterface()
    gen = TelegramJsonGenerator(json_path)
    ci.create_collection("roko-telegram", gen)
    print(
        f"Done: added {ci.count_collection(collection_name):,} docs to {collection_name} collection"
    )
