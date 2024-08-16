from data_collection.db_helpers import (
    get_single_data_from_db,
    persist_data_to_db,
    get_distict_values,
    get_all_data_from_db,
)

projects_collection_name = "all-projects"
issues_collection_name = "performance-issues"
issues_with_pr_collection_name = "performance-issues-with-pr"


def filter_performance_issues():
    issues = get_all_data_from_db(issues_collection_name)
    for issue in issues:
        pr_number = issue.get("pr_number", {})
        if pr_number:
            persist_data_to_db(issues_with_pr_collection_name, issue)


def filter_projects():
    project_names = get_distict_values(projects_collection_name, "full_name")
    issues_repo_names = get_distict_values(
        issues_with_pr_collection_name, "repo_fullname"
    )
    for project_name in project_names:
        if project_name in issues_repo_names:
            project = get_single_data_from_db(
                projects_collection_name, {"full_name": project_name}
            )
            persist_data_to_db("projects-with-issues", project)


filter_performance_issues()
filter_projects()
