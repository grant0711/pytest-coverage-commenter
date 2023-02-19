#!/usr/bin/env python
import sys

from github_api import (
    get_comment,
    create_comment,
    update_comment
)

def format_coverage_report(r):
    return r

def main(service_name, coverage_report, github_token, github_repo, github_issue_number):
    if github_issue_number == '0':
        return
    coverage_report = format_coverage_report(coverage_report)
    comment_id = get_comment(service_name, github_repo, github_token, github_issue_number)
    if not comment_id:
        create_comment(service_name, github_repo, github_token, github_issue_number, coverage_report)
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
