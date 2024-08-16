from pymongo import MongoClient, InsertOne


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
    source_db_name="final-first-research",
    source_collection_name="projects-refactorings",
    target_collection_name="projects-refactorings-clone-b",
)
