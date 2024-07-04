import time
from db_helpers import (
    get_all_data_from_db,
    update_data_in_db,
    count_data,
)
from github_api_helpers import get_issue_timeline, get_pr_commits

issues_collection_name = "performance-issues"


def get_performance_pull_requests():
    issues = get_all_data_from_db(issues_collection_name)
    total_issues = count_data(issues_collection_name)
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

                    if i % 30 == 0:
                        time.sleep(7)
                    break
        else:
            print(f"Issue #{issue['issue_number']} has no timeline")
            time.sleep(10)
            break


def get_performance_pull_request_commits():
    query = {}
    issues = get_all_data_from_db(issues_collection_name, query)
    total_issues = count_data(issues_collection_name, query)
    for i, issue in enumerate(issues, start=1):
        if i <= 15665:
            continue
        repo_fullname = issue["repo_fullname"]
        pr_number = issue.get("pr_number", None)
        print(
            f"======== Adding PR Commits for PR number: {pr_number} and Issue Number: {issue['issue_number']} for {repo_fullname} ========== ({i}/{total_issues})"
        )
        if not pr_number:
            continue
        pr_commits = get_pr_commits(repo_fullname, pr_number)
        commit_ids = []

        if not pr_commits:
            continue

        for index, commit in enumerate(pr_commits, start=1):
            if commit:
                commit_ids.append(commit["sha"])
        if commit_ids:
            update_data_in_db(
                issues_collection_name,
                issue["_id"],
                {"commit_ids": commit_ids},
            )
        if i % 50 == 0:
            time.sleep(7)
