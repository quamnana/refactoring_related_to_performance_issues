from pymongo import MongoClient
from bson.objectid import ObjectId
from data import projects

# Step 1: Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")

# Step 2: Access the database and project_refactorings_collection
db = client["research"]


def remove_non_performance_refactorings():
    """
    This function removes non-performance refactorings from a MongoDB collection and moves them to a new collection.
    It uses a list of repository fullnames to determine which refactorings to move.

    Parameters:
    None

    Returns:
    None
    """
    non_performance_refactorings_collection = db["non-performance-refactorings"]
    new_collection = db["non-performance-refactorings-new"]
    repo_fullnames = projects
    non_performance_refactorings = non_performance_refactorings_collection.find()

    total_names = len(repo_fullnames)
    moved = 0

    for index, non_perf_ref in enumerate(non_performance_refactorings, start=1):
        if non_perf_ref["repo_fullname"] in repo_fullnames:
            new_collection.insert_one(non_perf_ref)
            moved += 1
            print(
                f"Documents moved successfully with commit {non_perf_ref['commit_id']}  ====== {index} ===== {total_names}"
            )
    print(f"Total non-performance-refactorings removed: {moved}")


remove_non_performance_refactorings()
