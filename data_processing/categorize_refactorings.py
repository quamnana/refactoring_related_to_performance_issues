from pymongo import MongoClient
from bson.objectid import ObjectId


# Step 1: Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")

# Step 2: Access the database and project_refactorings_collection
db = client["final-first-research"]
project_refactorings_collection = db["projects-refactorings"]
all_performance_refactorings_collection = db["all-performance-refactorings"]
project_refactorings_backup_collection = db["projects-refactorings-backup"]
peformance_refactorings_collection = db["peformance-refactorings"]

# Step 3: Find all documents in all_performance_refactorings_collection
all_performance_refactorings = all_performance_refactorings_collection.find({})
total = all_performance_refactorings_collection.count_documents({})


def categorize_refactorings(all_performance_refactorings):
    index = 1
    for performance_refactoring in all_performance_refactorings:
        query = {
            "type": performance_refactoring["type"],
            "repo_fullname": performance_refactoring["repo_fullname"],
            "repo_name": performance_refactoring["repo_name"],
            "commit_id": performance_refactoring["commit_id"],
            "description": performance_refactoring["description"],
        }

        # Step 4: Check if the performance_refactoring from the all_performance_refactorings is in the project_refactorings_collection
        performance_refactoring_in_project = project_refactorings_collection.find_one(
            query
        )

        # Step 5: Print the found performance_refactoring_in_project
        if performance_refactoring_in_project:
            document_id = performance_refactoring_in_project["_id"]
            result = project_refactorings_backup_collection.delete_one(
                {"_id": ObjectId(document_id)}
            )

            # Step 6: Check if the performance_refactoring in the project_refactorings_backup_collection is removed then we insert that performance_refactoring into the peformance_refactorings_collection
            if result.deleted_count > 0:
                peformance_refactorings_collection.insert_one(performance_refactoring)

            print(
                f"Documents removed successfully with commit {performance_refactoring_in_project['commit_id']}  ====== {index}/{total}"
            )
        else:
            print(
                f"No performance_refactoring_in_project found with the specified criteria. ====== {index}/{total}"
            )

        index += 1


categorize_refactorings(all_performance_refactorings)
