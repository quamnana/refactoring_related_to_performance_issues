from projects_collection import *
from issues_collection import *
from prs_collection import *


def run_scripts():
    retrieve_java_projects()
    retrieve_java_project_details()
    get_performance_issues()
    get_performance_pull_requests()
    verify_collected_issues()


if __name__ == "__main__":
    run_scripts()
