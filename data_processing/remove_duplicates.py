from pymongo import MongoClient
import hashlib
import json

# Replace with your MongoDB connection string
mongo_uri = "mongodb://localhost:27017/"
database_name = "final-first-research"
collection_name = "all-performance-refactorings-using-commits-backup"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]


# Function to create a unique key from the document
def create_unique_key(doc):
    key_fields = {
        "type": doc["type"],
        "description": doc["description"],
        "leftSideLocations": doc["leftSideLocations"],
        "rightSideLocations": doc["rightSideLocations"],
        "commit_id": doc["commit_id"],
        "repo_name": doc["repo_name"],
        "repo_fullname": doc["repo_fullname"],
        "pr_number": doc["pr_number"],
        "perf_keyword": doc["perf_keyword"],
        "bug_keyword": doc["bug_keyword"],
        "issue_number": doc["issue_number"],
        "issue_title": doc["issue_title"],
    }
    # Convert the dictionary to a JSON string and hash it to create a unique key
    key_string = json.dumps(key_fields, sort_keys=True)
    unique_key = hashlib.md5(key_string.encode()).hexdigest()
    return unique_key


# Function to remove duplicates
def remove_duplicates():
    # Find all documents in the collection
    all_docs = list(collection.find())

    # Dictionary to track unique documents
    unique_docs = {}

    # Iterate through each document
    for doc in all_docs:
        # Create a unique key based on multiple fields
        unique_key = create_unique_key(doc)

        # Check if the unique key is already in the dictionary
        if unique_key not in unique_docs:
            unique_docs[unique_key] = doc["_id"]
        else:
            # If it's a duplicate, remove the document from the collection
            collection.delete_one({"_id": doc["_id"]})


if __name__ == "__main__":
    remove_duplicates()
    print("Duplicate documents removed.")
