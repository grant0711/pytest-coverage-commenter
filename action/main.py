#!/usr/bin/env python
import sys
import json

import requests



def github_session(github_token):
    """
    Description:
        - Instantiates a session object and updates headers of session

    Inputs:
        - github_token: str github token for authentication

    Outputs:
        - requests.Session() instance to be used within a context manager
    """
    s = requests.Session()
    s.headers.update({
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    })
    return s


def get_comment(service_name, github_repo, github_token, github_issue_number):
    """
    Description:
        - Gets up to 30 comments from an issue, iterates through each comment to identify
          a pre-existing coverage comment for a given service

    Inputs:
        - service_name: str name of service used to identify the coverage comment
        - github_repo: str format 'owner/repo' of the repository
        - github_token: str github token for authentication
        - github_issue_number: int github issue number

    Outputs:
        - int comment id if comment exists, None if does not exist

    Reference:
    https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28#list-issue-comments
    """
    with github_session(github_token) as s:
        response = s.get(
            url=f"https://api.github.com/repos/{github_repo}/issues/{github_issue_number}/comments"
        )
        if response.status_code != 200:
            raise Exception(f"Failed to get comment: {response.json()}; status_code: {response.status_code}")
        response_json = response.json()
        for comment in response_json:
            if comment.get('body', '').startswith(service_name + ' Coverage Report') and \
                comment.get('user', {}).get('login') == 'github-actions[bot]':
                return comment['id']
        return None


def create_comment(service_name, github_repo, github_token, github_issue_number, coverage_report):
    """
    Description:
        - Creates a new coverage comment on an issue

    Inputs:
        - service_name: str name of service used to identify the coverage comment
        - github_repo: str format 'owner/repo' of the repository
        - github_token: str github token for authentication
        - github_issue_number: int github issue number
        - coverage_report: str formatted coverage report to utilize as body of comment

    Outputs: None

    Side-Effects:
        - If a non-200 response status is returned from the call to Github API will raise an exception

    Reference:
    https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28#create-an-issue-comment
    """
    with github_session(github_token) as s:
        s.headers.update({'Content-Type': 'application/json'})
        response = s.post(
            url=f"https://api.github.com/repos/{github_repo}/issues/{github_issue_number}/comments",
            data=json.dumps({
                "body": service_name + " Coverage Report" + "\n\n" + coverage_report
            })
        )
        if response.status_code != 200:
            raise Exception(f"Failed to create comment: {response.json()}; status_code: {response.status_code}")
    return


def update_comment(service_name, github_repo, github_token, comment_id, coverage_report):
    """
    Description:
        - Updates an existing coverage comment on an issue

    Inputs:
        - service_name: str name of service used to identify the coverage comment
        - github_repo: str format 'owner/repo' of the repository
        - github_token: str github token for authentication
        - comment_id: int github comment id of existing coverage comment
        - coverage_report: str formatted coverage report to utilize as body of comment

    Outputs: None

    Side-Effects:
        - If a non-200 response status is returned from the call to Github API will raise an exception

    Reference:
    https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28#update-an-issue-comment
    """
    with github_session(github_token) as s:
        s.headers.update({'Content-Type': 'application/json'})
        response = s.patch(
            url=f"https://api.github.com/repos/{github_repo}/issues/comments/{comment_id}",
            data=json.dumps({
                "body": service_name + " Coverage Report" + "\n\n" + coverage_report
            })
        )
        if response.status_code != 200:
            raise Exception(f"Failed to update comment: {response.json()}; status_code: {response.status_code}")
    return


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
