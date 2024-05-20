import requests

from env import JIRA_ACCESS_TOKEN

# Define the Jira server URL and API endpoint
jira_url = "https://jira.atlassian.com/rest/api/2/search"

# Set up authentication credentials
username = "quamgyambrah@gmail.com"
api_token = JIRA_ACCESS_TOKEN  # You can generate an API token in Jira settings

# Define the JQL query to search for issues related to Hadoop
jql_query = "project = HDFS"

# Set up the request headers with authentication information
headers = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer " + JIRA_ACCESS_TOKEN,
}

# Set up the query parameters
params = {
    "jql": jql_query,
    "maxResults": 50,  # Adjust as needed to limit the number of results returned
}

# Make the HTTP request to the Jira API
response = requests.get(
    jira_url, params=params, auth=(username, api_token), headers=headers
)


# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract and print the issues from the response JSON
    issues = response.json()["issues"]
    for issue in issues:
        print(issue["key"], "-", issue["fields"]["summary"])
else:
    print("Failed to retrieve issues. Status code:", response.status_code)
    print(response)
