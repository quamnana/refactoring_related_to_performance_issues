import time
from db_helpers import persist_data_to_db, get_all_data_from_db, update_data_in_db
from github_api_helpers import (
    get_java_project_details,
    get_closed_issue_and_pr_count,
    search_java_projects,
)

STARS_COUNT = [20 + i * 100 if i <= 9 else 1000 + (i - 9) * 10 for i in range(0, 1000)]
collection_name = "java-projects"


def retrieve_java_projects():

    for index, count in enumerate(STARS_COUNT):
        page = 1
        least_stars = STARS_COUNT[index]
        most_stars = STARS_COUNT[index + 1]
        print(
            f"======== GETTING JAVA PROJECTS FOR STARS FROM {least_stars} TO {most_stars} ========="
        )
        while True:
            java_projects = search_java_projects(page, least_stars, most_stars)
            if java_projects:
                for repo in java_projects:
                    data_to_persist = {
                        "repo_id": repo["id"],
                        "node_id": repo["node_id"],
                        "name": repo["name"],
                        "full_name": repo["full_name"],
                        "language": repo["language"],
                        "stargazers_count": repo["stargazers_count"],
                    }
                    persist_data_to_db(collection_name, data_to_persist)
                page = page + 1
                time.sleep(5)
            else:
                print("Failed to fetch Java projects from GitHub.")
                time.sleep(20)
                break


def retrieve_java_project_details():

    # get projects from mongodb
    java_projects = get_all_data_from_db(collection_name)

    # use full_name of each project to get project details
    for index, project in enumerate(java_projects, start=1):
        has_open_issue = project.get("open_issues", None)
        if has_open_issue is not None:
            continue

        full_name = project["full_name"]
        owner, repo = full_name.split("/")
        id = project["_id"]

        print(f"Getting details of {full_name}")

        project_details = get_java_project_details(full_name)
        if project_details:
            total_closed_issues, total_closed_pull_requests = (
                get_closed_issue_and_pr_count(owner, repo)
            )

            data_to_persist = {
                "repo_id": project_details["id"],
                "node_id": project_details["node_id"],
                "name": project_details["name"],
                "full_name": project_details["full_name"],
                "url": project_details["url"],
                "html_url": project_details["html_url"],
                "stargazers_count": project_details["stargazers_count"],
                "watchers_count": project_details["watchers_count"],
                "watchers": project_details["watchers"],
                "size": project_details["size"],
                "default_branch": project_details["default_branch"],
                "open_issues_count": project_details["open_issues_count"],
                "open_issues": project_details["open_issues"],
                "has_issues": project_details["has_issues"],
                "closed_issues_count": total_closed_issues,
                "closed_prs_count": total_closed_pull_requests,
                "total_issue_and_prs": total_closed_issues + total_closed_pull_requests,
            }
            update_data_in_db(collection_name, id, data_to_persist)

            # this is to make sure the GitHub API rate limit is not exceeded
            if index % 50 == 0:
                time.sleep(20)
        else:
            time.sleep(10)
            continue
