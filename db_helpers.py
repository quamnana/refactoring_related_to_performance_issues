from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["first-research"]


def persist_data_to_db(collection_name, data):
    collection = db[collection_name]
    try:
        data_id = collection.insert_one(data).inserted_id
        print("Successfully persisted data at ID: ", data_id)
    except Exception as e:
        print("Failed to persist data: ", e)


def get_all_data_from_db(collection_name):
    collection = db[collection_name]
    try:
        data = collection.find()
        print("Successfully fetched data")
        return data
    except:
        print("Failed to fetch data")


def update_data_in_db(collection_name, id, data):
    collection = db[collection_name]
    try:
        filter = {"_id": id}
        update = {"$set": data}
        collection.update_one(filter, update)
        print("Successfully updated data for ID: ", id)
    except:
        print("Failed to update")
