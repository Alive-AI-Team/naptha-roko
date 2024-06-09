## Chroma Vector Database

First start the chroma server with:
```
chroma run ./chroma.db
```

By default this will run the server on `localhost:8000`

### Create Collection

A collection consists of records each containing a short `text` string with meta data `date` posted, and `from_id` given the username of the person who posted the message, as well as an id for the message.

The input data in this example is designed around a Telegram chat export JSON format, which looks like this:
```
{
 "name": "ᎡOKO Network",
 "type": "private_supergroup",
 "id": 1881240854,
 "messages": [
   {
   "id": 1,
   "type": "service",
   "date": "2023-03-04T00:30:51",
   "date_unixtime": "1677861051",
   "actor": "ᎡOKO Network",
   "actor_id": "channel1881240854",
   "action": "migrate_from_group",
   "title": "Roko Network",
   "text": "",
   "text_entities": []
    ...
   },
 ]
}
```

There is a lot of junk, short messages, with little information content. We therefore only insert messages of a minimum length into the vector db: 100 characters by default.

`create_collection.py` will create a Chroma database with a collection containing this data, using the `ChromaInterface`. Note: you can only run `create_collection.py` once as it creates 
a collection: if you want to re-run it just delete the chroma database first. It is recommended that you have a GPU for creating the collection as it calcs the embeddings.

### Testing the Collection

The script `query_collection.py` runs a query against the collection and return the results.

An example output would be:
```
Collection has 4,493 documents.
{
  "ids": [
    [
      "43779",
      "52391",
      "43764"
    ]
  ],
  "distances": [
    [
      0.31367552280426025,
      0.32932156324386597,
      0.34631502628326416
    ]
  ],
  "embeddings": null,
  "metadatas": [
    [
      {
        "date": "2023-06-20T15:58:38",
        "from_id": "user6014099426"
      },
      {
        "date": "2023-09-07T22:04:01",
        "from_id": "user1636455540"
      },
      {
        "date": "2023-06-20T12:13:04",
        "from_id": "user674728722"
      }
    ]
  ],
  "documents": [
    [
      "glad to talk if anyone is confused about stuff or needs a general direction of what Roko Network is and where it is going.",
      "i dont understand the Roko network, what is the   really good usecase of it? And which problem will roko will resolve",
      "Ngl, we need better marketing material that explains Roko Network. Waiting on that website update and white paper. The guy took a good guess at it with what he could easily find."
    ]
  ],
  "uris": null,
  "data": null
}
```