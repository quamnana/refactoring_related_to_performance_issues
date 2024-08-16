from pymongo import MongoClient
from bson.objectid import ObjectId
from data import projects


# Step 1: Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")

# Step 2: Access the database and project_refactorings_collection
db = client["final-first-research"]
project_refactorings_collection = db["projects-refactorings"]
all_performance_refactorings_collection = db[
    "all-performance-refactorings-using-commits-backup"
]
project_refactorings_clone_collection = db["projects-refactorings-clone-b"]
initial_performance_refactorings = db[
    "performance-refactorings-from-projects-refactorings-b"
]


performance_refactorings_collection = db["performance-refactorings-b"]
peformance_issues_collection = db["performance-issues"]

# Step 3: Find all documents in all_performance_refactorings_collection
all_performance_refactorings = all_performance_refactorings_collection.find({})
total = all_performance_refactorings_collection.count_documents({})


def categorize_refactorings(all_performance_refactorings):
    index = 1
    for performance_refactoring in all_performance_refactorings:
        query = {
            "type": performance_refactoring["type"],
            "repo_fullname": performance_refactoring["repo_fullname"],
            # "repo_name": performance_refactoring["repo_name"],
            "commit_id": performance_refactoring["commit_id"],
            # "description": performance_refactoring["description"],
        }

        # Step 4: Check if the performance_refactoring from the all_performance_refactorings is in the project_refactorings_collection
        performance_refactoring_in_project = project_refactorings_collection.find_one(
            query
        )

        # Step 5: Print the found performance_refactoring_in_project
        if performance_refactoring_in_project:
            document_id = performance_refactoring_in_project["_id"]
            result = project_refactorings_clone_collection.delete_one(
                {"_id": ObjectId(document_id)}
            )

            # Step 6: Check if the performance_refactoring in the project_refactorings_clone_collection is removed then we insert that performance_refactoring into the initial_performance_refactorings
            if result.deleted_count > 0:
                initial_performance_refactorings.insert_one(performance_refactoring)

            print(
                f"Documents removed successfully with commit {performance_refactoring_in_project['commit_id']}  ====== {index}/{total}"
            )
        else:
            print(
                f"No performance_refactoring_in_project found with the specified criteria. ====== {index}/{total}"
            )

        index += 1

    # Step 7: Rename the collection
    # db[project_refactorings_clone_collection].rename("non-performance-refactorings-b")

    # # Step 8: extract performance refactorings related to performance issues
    # extract_performance_refactorings_related_to_performance_issues()


def extract_performance_refactorings_related_to_performance_issues():
    # Fetch issues with commit Ids
    issues_related_to_performance_refactorings = list(
        peformance_issues_collection.find(
            {"commit_ids": {"$exists": True, "$ne": None}}, {"commit_ids": 1}
        )
    )
    print(
        f"Total number of issues related to performance refactorings: {len(issues_related_to_performance_refactorings)}"
    )

    # Extract commit IDs for each issue
    commit_ids = []
    for issue in issues_related_to_performance_refactorings:
        issue_commit_ids = issue.get("commit_ids", [])
        commit_ids.extend(issue_commit_ids)

    print(
        f"Total number of commit IDs extracted from performance issues: {len(commit_ids)}"
    )

    query = {"commit_id": {"$in": commit_ids}}

    # Fetch performance refactorings with commit IDs in the performance issues collection
    performance_refactorings = list(initial_performance_refactorings.find(query))

    # Print the total number of performance refactorings
    print(
        f"Total number of performance refactorings found: {len(performance_refactorings)}"
    )

    # Insert performance refactorings into the performance_refactorings_collection
    performance_refactorings_collection.insert_many(performance_refactorings)
    print(f"Performance refactorings inserted successfully")


extract_performance_refactorings_related_to_performance_issues()
