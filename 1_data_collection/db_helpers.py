from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["research"]


def persist_data_to_db(collection_name, data):
    collection = db[collection_name]
    try:
        data_id = collection.insert_one(data).inserted_id
        print("Successfully persisted data at ID: ", data_id)
    except Exception as e:
        print("Failed to persist data: ", e)


def get_all_data_from_db(collection_name, query={}):
    collection = db[collection_name]
    try:
        data = collection.find(query)
        print("Successfully fetched data")
        return data
    except:
        print("Failed to fetch data")


def get_single_data_from_db(collection_name, query={}):
    collection = db[collection_name]
    try:
        data = collection.find_one(query)
        print("Successfully fetched data")
        return data
    except:
        print("Failed to fetch data")


def count_data(collection_name, query={}):
    collection = db[collection_name]
    try:
        count = collection.count_documents(query)
        return count
    except:
        print("Failed to get count of data")


def update_data_in_db(collection_name, id, data):
    collection = db[collection_name]
    try:
        filter = {"_id": id}
        update = {"$set": data}
        collection.update_one(filter, update)
        print("Successfully updated data for ID: ", id)
    except:
        print("Failed to update")


def get_distict_values(collection_name, field_name):
    collection = db[collection_name]
    try:
        distict_values = collection.distinct(field_name)
        return distict_values
    except:
        print("Failed to get distinct values")
