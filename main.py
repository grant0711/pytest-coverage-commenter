#!/usr/bin/env python
import sys

from github_api import (
    get_comment,
    create_comment,
    update_comment
)

def format_coverage_report(r):
    print(r)
    return r

def main(service_name, coverage_report, github_token, github_repo, github_issue_number):
    # Check to make sure we are on a pull request and not a push
    if github_issue_number == '0':
        return

    # Format the coverage report
    coverage_report = format_coverage_report(coverage_report)

    # Find existing comment
    comment_id = get_comment(service_name, github_repo, github_token, github_issue_number)
    print(comment_id)

    # If not found, create one
    if not comment_id:
        create_comment(service_name, github_repo, github_token, github_issue_number, coverage_report)

    # If found, update the existing one
    else:
        update_comment(service_name, github_repo, github_token, comment_id, coverage_report)


if __name__=="__main__":
    main(
        service_name = sys.argv[1],
        coverage_report = sys.argv[2],
        github_token = sys.argv[3],
        github_repo = sys.argv[4],
        github_issue_number = sys.argv[5]
    )
