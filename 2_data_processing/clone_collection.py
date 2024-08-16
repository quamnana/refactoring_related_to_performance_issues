from pymongo import MongoClient, InsertOne

"""
    This function clones a collection from a source MongoDB database to a target MongoDB database.

    Parameters:
    source_db_name (str): The name of the source MongoDB database.
    source_collection_name (str): The name of the source MongoDB collection.
    target_collection_name (str): The name of the target MongoDB collection.
    uri (str): The MongoDB connection URI. Default is "mongodb://localhost:27017/".
    batch_size (int): The number of documents to insert in a single batch. Default is 5000.

    Returns:
    None. The function prints the progress of cloning and the final message.
"""


def clone_collection(
    source_db_name,
    source_collection_name,
    target_collection_name,
    uri="mongodb://localhost:27017/",
    batch_size=5000,
):
    client = MongoClient(uri)

    # Source and target database and collection
    source_db = client[source_db_name]
    source_collection = source_db[source_collection_name]
    target_db = client[source_db_name]
    target_collection = target_db[target_collection_name]

    # Remove existing documents in target collection if necessary
    target_collection.delete_many({})

    # Copy all documents from source to target collection in batches
    documents = source_collection.find()
    batch = []
    count = 0
    total_docs = source_collection.count_documents({})

    for doc in documents:
        batch.append(InsertOne(doc))
        count += 1
        if len(batch) == batch_size:
            target_collection.bulk_write(batch)
            print(f"Inserted {count} of {total_docs} documents.")
            batch = []

    # Write any remaining documents in the batch
    if batch:
        target_collection.bulk_write(batch)
        print(f"Inserted {count} of {total_docs} documents.")

    print(
        f"Cloned {source_collection_name} from {source_db_name} to {target_collection_name} in {source_db_name}"
    )


clone_collection(
    source_db_name="research",
    source_collection_name="projects-refactorings",
    target_collection_name="projects-refactorings-clone",
)
