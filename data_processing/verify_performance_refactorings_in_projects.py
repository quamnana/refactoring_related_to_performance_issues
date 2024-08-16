from pymongo import MongoClient
import webbrowser

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Access the specified database
db = client["final-first-research"]


def get_distinct_fields(collection_name, field):
    collection = db[collection_name]
    distinct_fields = collection.distinct(field)
    print(distinct_fields)
    return distinct_fields


def get_refactorings_not_found_in_projects():
    repo_fullnames = get_distinct_fields(
        "non-performance-refactorings-new", "repo_fullname"
    )
    query = {"repo_fullname": {"$nin": repo_fullnames}}
    pipeline = [
        {"$match": query},
        {
            "$project": {
                "description": 0,
                "leftSideLocations": 0,
                "rightSideLocations": 0,
            }
        },
        {"$sample": {"size": 10}},
    ]
    collection = db["all-performance-refactorings"]
    ref_not_found_in_projects = list(collection.aggregate(pipeline))
    return ref_not_found_in_projects


def get_refactorings_performance_issues():
    refactorings = get_refactorings_not_found_in_projects()
    collection = db["performance-issues"]
    issues = []
    for ref in refactorings:
        query = {"repo_fullname": ref["repo_fullname"], "pr_number": ref["pr_number"]}
        issue = collection.find_one(query)
        issues.append(issue)
    return issues


def view_refactorings():
    """
    This function retrieves performance issues related to refactorings not found in projects,
    opens the corresponding GitHub pull request URLs in a web browser, and allows the user to proceed
    to the next issue by pressing Enter.

    Parameters:
    None

    Returns:
    None
    """
    issues = get_refactorings_performance_issues()
    # Iterate through each project
    for count, issue in enumerate(issues, start=1):
        # Extract the URL from the issue
        print(issue["repo_default_branch"])
        html_url = issue.get("pr_url")
        if html_url:
            print(f"Opening URL: {html_url} ================== {count}")
            webbrowser.open(html_url)
            input("Press Enter to proceed to the next issue...")
        else:
            print("No 'html_url' found in issue, skipping...")


view_refactorings()
