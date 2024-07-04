from data_collection.projects_extraction import *
from data_collection.performance_issues_extraction import *
from data_collection.pull_requests_extraction import *


def run_scripts():
    retrieve_projects()
    retrieve_projects_details()
    get_performance_issues()
    get_performance_pull_requests()
    get_performance_pull_request_commits()
    verify_collected_issues()


if __name__ == "__main__":
    run_scripts()
