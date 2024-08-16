# This script is used to extract some projects (50) without performance and verify from GitHub if they truly didnt have performance issues in their repos.

from pymongo import MongoClient
import webbrowser

from data_collection.db_helpers import get_distict_values, get_all_data_from_db

# Replace the following with your MongoDB connection details
mongo_uri = "mongodb://localhost:27017/"
database_name = "research-data"
projects_collection_name = "all-projects"
issues_collection_name = "performance-issues"
limit = 50

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[projects_collection_name]

distinct_projects_in_performance_issues = get_distict_values(
    issues_collection_name, "repo_fullname"
)

query = {"full_name": {"$nin": distinct_projects_in_performance_issues}}
projects = collection.find().limit(limit)


# Function to open URL in web browser
def open_url(url):
    webbrowser.open(url)


# Iterate through each project
for count, project in enumerate(projects, start=1):
    # Extract the URL from the project
    html_url = project.get("html_url")
    if html_url:
        print(f"Opening URL: {html_url} ================== {count}")
        open_url(html_url)
        input("Press Enter to proceed to the next project...")
    else:
        print("No 'html_url' found in project, skipping...")
