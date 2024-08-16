import os
import json
import re
from pymongo import MongoClient

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "research-data"
COLLECTION_NAME = "projects-refactorings"
# JSON_DIRECTORY = "/Users/nanaquam/Library/CloudStorage/GoogleDrive-quamgyambrah@gmail.com/My Drive/refactoring_miner_all_projects_results"
JSON_DIRECTORY = "data_collection/project_refactorings_extraction/results"


# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


"""
    This function iterates over all JSON files in the specified directory,
    loads the data from each file, and inserts it into a MongoDB database.

    Parameters:
    None

    Returns:
    None

    Raises:
    None
"""


def load_json_to_db():
    # Iterate over all JSON files in the specified directory
    files = os.listdir(JSON_DIRECTORY)
    total = len(files)
    for index, filename in enumerate(files, start=1):
        filepath = os.path.join(JSON_DIRECTORY, filename)
        if filename.endswith(".json"):
            with open(filepath, "r") as file:
                try:
                    data = json.load(file)
                    print(
                        f" {index} =================================== ================= GETTING DATA FOR ================================================ {filename}"
                    )
                    try:
                        restructure_data(data)
                    except Exception as e:
                        log_error(filename, str(e), index)
                        continue
                    print(
                        f"============================================ Inserted data from {filename} into MongoDB ============================================= {index} / {total}"
                    )
                    log_success(filename, index)
                except json.JSONDecodeError as e:
                    print(f"Failed to decode JSON from file {filename}")
                    log_error(filename, str(e), index)
        else:
            log_error(filename, "The file was not valid", index)


"""
    This function processes the given data, which contains information about commits and refactorings.
    It extracts relevant information from the commits and refactorings, and restructures the data for easier storage in a database.

    Parameters:
    data (dict): A dictionary containing information about commits and refactorings.
    Returns:
    None
 """


def restructure_data(data):
    commits = data.get("commits", None)
    if commits:
        total_commits = len(commits)
        for commit_index, commit in enumerate(commits, start=1):
            print_log = f"-------------------------- {commit_index}/{total_commits}"

            repo = commit["repository"]
            commit_id = commit["sha1"]
            repo_fullname, repo_name = extract_repo_parts(repo)

            refactorings = commit.get("refactorings", [])
            if refactorings:
                for ref_index, refactoring in enumerate(refactorings, start=1):
                    refactoring["repo_name"] = repo_name
                    refactoring["repo_fullname"] = repo_fullname
                    refactoring["commit_id"] = commit_id
                    persist_data_to_db(refactoring, print_log)
            else:
                no_ref = {}
                no_ref["repo_name"] = repo_name
                no_ref["repo_fullname"] = repo_fullname
                no_ref["commit_id"] = commit_id
                no_ref["type"] = None
                no_ref["description"] = None
                no_ref["leftSideLocations"] = []
                no_ref["rightSideLocations"] = []
                persist_data_to_db(no_ref, print_log)


"""
    Extracts the user/repo and repository name parts from a given GitHub repository URL.

    Parameters:
    url (str): The GitHub repository URL. It should be in the format "https://github.com/user/repo.git".

    Returns:
    tuple: A tuple containing two strings: the "user/repo" part and the repository name.
           If the URL does not match the expected format, both parts will be None.
"""


def extract_repo_parts(url):
    # Remove the .git suffix
    clean_url = re.sub(r"\.git$", "", url)

    # Extract the "user/repo" part
    user_repo_match = re.search(r"github\.com/([^/]+/[^/]+)", clean_url)
    user_repo = user_repo_match.group(1) if user_repo_match else None

    # Extract the repository name
    repo_match = re.search(r"github\.com/[^/]+/([^/]+)", clean_url)
    repo_name = repo_match.group(1) if repo_match else None

    return user_repo, repo_name


def persist_data_to_db(data, log):
    # collection = db[collection_name]
    try:
        data_id = collection.insert_one(data).inserted_id
        print("Successfully persisted data at ID: ", data_id, log)
    except Exception as e:
        print("Failed to persist data: ", e)


def log_error(filename, error_message, index):
    with open("logs/error.txt", "a") as error_log:
        error_log.write(f"Error in file {filename} - {index}: {error_message}\n")


def log_success(filename, index):
    with open("logs/success.txt", "a") as error_log:
        error_log.write(f"Successfully inserted file {filename} to mongodb: {index}\n")


if __name__ == "__main__":
    load_json_to_db()
