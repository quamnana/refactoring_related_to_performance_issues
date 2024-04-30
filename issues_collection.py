import time
from db_helpers import (
    get_all_data_from_db,
    persist_data_to_db,
    update_data_in_db,
    get_distict_values,
)
from github_api_helpers import search_performance_issues, get_issue_timeline

projects_collection_name = "java-projects"
issues_collection_name = "performance-issues"


def get_performance_issues():
    java_projects = get_all_data_from_db(projects_collection_name)
    total_projects = 3187
    performance_keywords = [
        "performance",
        "fast",
        "slow",
        "perform",
        "latency",
        "throughput",
        "optimize",
        "speed",
        "heuristic",
        "waste",
        "efficient",
        "execution",
        "too many times",
        "lot of time",
        "too much time",
        "caching",
    ]

    bug_keywords = [
        "error",
        "bug",
        "issue",
        "mistake",
        "incorrect",
        "fault",
        "defect",
        "flaw",
    ]

    for i, project in enumerate(java_projects, start=1):
        full_name = project["full_name"]
        if i in range(102):
            continue
        for perf_keyword in performance_keywords:
            for bug_keyword in bug_keywords:

                page = 1
                print(
                    f"================= FETCHING ISSUES FOR {project['name']} WITH PERFORMANCE KEYWORD [[{perf_keyword}]] AND BUG KEYWORD [[{bug_keyword}]] ========================= ({i}/{total_projects})"
                )
                print(full_name)
                while True:
                    # Search for issues related to performance
                    search_query = f'"{perf_keyword}" repo:{full_name} {bug_keyword} in:title,body,comments is:closed linked:pr'

                    issues = search_performance_issues(search_query, page)
                    if issues:
                        for index, issue in enumerate(issues, start=1):
                            print(
                                f"{index}. Project: {project['name']} - Issue# {issue['number']}- {issue['title']}"
                            )
                            repo_id = project["repo_id"]
                            repo_node_id = project["node_id"]
                            repo_name = project["name"]
                            repo_fullname = project["full_name"]
                            repo_url = project["html_url"]
                            repo_default_branch = project["default_branch"]
                            issue_number = issue["number"]
                            issue_title = issue["title"]
                            issue_created_at = issue["created_at"]
                            issue_closed_at = issue["closed_at"]
                            issue_url = issue["html_url"]
                            issue_api_url = issue["url"]
                            issue_labels = [label["name"] for label in issue["labels"]]
                            issue_timeline_url = issue["timeline_url"]

                            data_to_persist = {
                                "repo_id": repo_id,
                                "repo_node_id": repo_node_id,
                                "repo_name": repo_name,
                                "repo_fullname": repo_fullname,
                                "repo_url": repo_url,
                                "repo_default_branch": repo_default_branch,
                                "issue_number": issue_number,
                                "issue_title": issue_title,
                                "issue_url": issue_url,
                                "issue_api_url": issue_api_url,
                                "issue_labels": issue_labels,
                                "issue_created_at": issue_created_at,
                                "issue_closed_at": issue_closed_at,
                                "issue_timeline_url": issue_timeline_url,
                                "perf_keyword": perf_keyword,
                                "bug_keyword": bug_keyword,
                            }
                            persist_data_to_db(issues_collection_name, data_to_persist)
                        if len(issues) >= 50:
                            page = page + 1
                            if bug_keyword == "flaw":
                                time.sleep(10)
                        else:
                            time.sleep(5)
                            break
                    else:
                        print(
                            f"Failed to fetch project issues for performance keyword {perf_keyword} and bug keyword {bug_keyword} at page {page} from GitHub."
                        )
                        if bug_keyword == "flaw":
                            time.sleep(10)
                        break


def get_performance_pull_requests():
    issues = get_all_data_from_db(issues_collection_name)
    total_issues = 0
    for i, issue in enumerate(issues, start=1):
        issue_timeline_url = issue["issue_timeline_url"]
        issue_timeline = get_issue_timeline(issue_timeline_url)
        if issue_timeline:
            for event in issue_timeline:
                if (
                    event.get("event") == "cross-referenced"
                    and event.get("source", {}).get("issue", {}).get("state")
                    == "closed"
                ):
                    pr_url = event["source"]["issue"]["html_url"]
                    pr_title = event["source"]["issue"]["title"]
                    pr_number = event["source"]["issue"]["number"]
                    pr_api_url = event["source"]["issue"]["url"]
                    pr_created_at = event["source"]["issue"]["created_at"]
                    pr_updated_at = event["source"]["issue"]["updated_at"]
                    pr_closed_at = event["source"]["issue"]["closed_at"]
                    pr_merged_at = (
                        event["source"]["issue"]
                        .get("pull_request", {})
                        .get("merged_at")
                    )
                    _pr_labels = event["source"]["issue"]["labels"]
                    pr_labels = [label["name"] for label in _pr_labels]

                    print(
                        f"======== The issue #{issue['issue_number']} was closed by Pull Request - Title: {pr_title} URL: {pr_url} ========== ({i}/{total_issues})"
                    )
                    data_to_persist = {
                        "pr_number": pr_number,
                        "pr_title": pr_title,
                        "pr_url": pr_url,
                        "pr_api_url": pr_api_url,
                        "pr_created_at": pr_created_at,
                        "pr_updated_at": pr_updated_at,
                        "pr_closed_at": pr_closed_at,
                        "pr_merged_at": pr_merged_at,
                        "pr_labels": pr_labels,
                    }
                    update_data_in_db(
                        issues_collection_name, issue["_id"], data_to_persist
                    )
                    time.sleep(10)
                    break
        else:
            print(f"Issue #{issue['issue_number']} has no timeline")
            time.sleep(10)
            break


def verify_collected_issues():
    results = {}
    project_names = get_distict_values(projects_collection_name, "full_name")
    issues_repo_names = get_distict_values(issues_collection_name, "repo_fullname")
    for project_name in project_names:
        if project_name in issues_repo_names:
            results[project_name] = True
        else:
            results[project_name] = False
    print(results)


def main():
    get_performance_issues()
    # get_performance_pull_requests()
    # verify_collected_issues()


main()
