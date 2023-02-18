#!/usr/bin/env python
import sys

import requests



def format_coverage_report(r):
    print(r)
    return r

def get_comment(service_name, github_repo, github_token, github_issue_number):
    return ''

def create_comment(service_name, github_repo, github_token, github_issue_number, coverage_report):
    return

def update_comment(service_name, github_repo, github_token, github_issue_number, coverage_report):
    return

def main():
    service_name = sys.argv[1]
    coverage_report = sys.argv[2]
    github_token = sys.argv[3]
    github_repo = sys.argv[4]
    github_issue_number = sys.argv[5]

    # Check to make sure we are on a pull request and not a push
    print(github_issue_number)
    print(type(github_issue_number))
    if github_issue_number == 0:
        return

    # Format the coverage report
    coverage_report = format_coverage_report(coverage_report)

    # Find existing comment
    comment_id = get_comment(service_name, github_repo, github_token, github_issue_number)

    # If not found, create one
    if not comment_id:
        create_comment(service_name, github_repo, github_token, github_issue_number, coverage_report)

    # If found, update the existing one
    else:
        update_comment(service_name, github_repo, github_token, github_issue_number, coverage_report)




if __name__=="__main__":
    main()

    
# Where to find a comment:
# GET
# https://api.github.com/repos/{owner}/{repo}/issues/{pull number}/comments
# https://api.github.com/repos/grant0711/talk_to_me/issues/1/comments


# Iterate through all pages to find a comment with the body that matches our coverage
# report, if it doesn't find it then there isn't already a coverage comment

# Update a comment:

# PATCH
# https://api.github.com/repos/{owner}/{repo}/issues/comments/{comment_id}
# https://api.github.com/repos/grant0711/talk_to_me/issues/comments/1435650589

# payload = {"body": "desired new comment body"}

# Create a new comment:

# POST
# https://api.github.com/repos/{owner}/{repo}/issues/{issue number}/comments

# payload = {"body": "desired new comment body"}
