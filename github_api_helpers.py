import requests
from env import ACCESS_TOKEN

def search_java_projects_with_jmh( page):
    url = "https://api.github.com/search/code"
    params = {
        "q": "filename:pom.xml jmh-core in:file",
        "sort": "stars",
        "order": "desc",
        "per_page": 100,
        "page": page,
    }
    headers = {"Authorization": f"token {ACCESS_TOKEN}"}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for 4XX and 5XX status codes
        data = response.json()
        return data["items"]
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


def get_java_project_details(full_name):
    url = f"https://api.github.com/repos/{full_name}"
    headers = {"Authorization": f"token {ACCESS_TOKEN}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4XX and 5XX status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


def get_closed_issue_and_pr_count(owner, repo):
    query = """
    query {
      repository(owner: "%s", name: "%s") {
        issues(states: CLOSED) {
          totalCount
        }
        pullRequests(states: CLOSED) {
          totalCount
        }
      }
    }
    """ % (
        owner,
        repo,
    )

    headers = {"Authorization": "Bearer " + ACCESS_TOKEN}

    response = requests.post(
        "https://api.github.com/graphql", json={"query": query}, headers=headers
    )
    if response.status_code == 200:
        data = response.json()
        total_closed_issues = data["data"]["repository"]["issues"]["totalCount"]
        total_closed_pull_requests = data["data"]["repository"]["pullRequests"][
            "totalCount"
        ]
        return total_closed_issues, total_closed_pull_requests
    else:
        print("Failed to fetch data:", response.status_code)
        return None, None


def search_performance_issues(query, page):
    # Define the GitHub API endpoint for searching issues
    url = "https://api.github.com/search/issues"

    # Define the parameters for the search query
    params = {"q": query, "per_page": 50, "page": page}

    # Make a GET request to the GitHub API
    # response = requests.get(url, params=params)

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for 4XX and 5XX status codes
        data = response.json()
        return data["items"]
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


def get_issue_timeline(url):

    headers = {"Authorization": f"token {ACCESS_TOKEN}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4XX and 5XX status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
