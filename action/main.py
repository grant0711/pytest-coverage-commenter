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


def get_comment(service_name, github_repo, github_issue_number, session):
    """
    Description:
        - Gets up to 30 comments from an issue, iterates through each comment to identify
          a pre-existing coverage comment for a given service

    Inputs:
        - service_name: str name of service used to identify the coverage comment
        - github_repo: str format 'owner/repo' of the repository
        - github_issue_number: int github issue number

    Outputs:
        - int comment id if comment exists, None if does not exist

    Reference:
    https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28#list-issue-comments
    """
    response = session.get(
        url=f"https://api.github.com/repos/{github_repo}/issues/{github_issue_number}/comments"
    )
    if 200 <= response.status_code <= 299:
        response_json = response.json()
        for comment in response_json:
            if comment.get('body', '').startswith('# ' + service_name + ' Coverage Report') and \
                comment.get('user', {}).get('login') == 'github-actions[bot]':
                return comment['id']
        return None
    raise Exception(f"Failed to get comment: {response.json()}; status_code: {response.status_code}")


def create_comment(service_name, github_repo, github_issue_number, coverage_report, session):
    """
    Description:
        - Creates a new coverage comment on an issue

    Inputs:
        - service_name: str name of service used to identify the coverage comment
        - github_repo: str format 'owner/repo' of the repository
        - github_issue_number: int github issue number
        - coverage_report: str formatted coverage report to utilize as body of comment

    Outputs: None

    Side-Effects:
        - If a non-200 response status is returned from the call to Github API will raise an exception

    Reference:
    https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28#create-an-issue-comment
    """
    session.headers.update({'Content-Type': 'application/json'})
    response = session.post(
        url=f"https://api.github.com/repos/{github_repo}/issues/{github_issue_number}/comments",
        data=json.dumps({
            "body": titled_coverage_report(service_name, coverage_report)
        })
    )
    if 200 <= response.status_code <= 299:
        return    
    raise Exception(f"Failed to create comment: {response.json()}; status_code: {response.status_code}")


def update_comment(service_name, github_repo, comment_id, coverage_report, session):
    """
    Description:
        - Updates an existing coverage comment on an issue

    Inputs:
        - service_name: str name of service used to identify the coverage comment
        - github_repo: str format 'owner/repo' of the repository
        - comment_id: int github comment id of existing coverage comment
        - coverage_report: str formatted coverage report to utilize as body of comment

    Outputs: None

    Side-Effects:
        - If a non-200 response status is returned from the call to Github API will raise an exception

    Reference:
    https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28#update-an-issue-comment
    """
    session.headers.update({'Content-Type': 'application/json'})
    response = session.patch(
        url=f"https://api.github.com/repos/{github_repo}/issues/comments/{comment_id}",
        data=json.dumps({
            "body": titled_coverage_report(service_name, coverage_report)
        })
    )
    if 200 <= response.status_code <= 299:
        return
    raise Exception(f"Failed to update comment: {response.json()}; status_code: {response.status_code}")


def strip_line(v):
    return v != '----------------------------------------'


def format_coverage_report(r):
    """
    Description:
        - Takes as input the coverage report and transforms into a more user-friendly format for
          the coverage comment body

    Inputs:
        - r: str coverage report
    Outputs:
        - str formatted coverage report with only 'Name' and 'Cover' columns and newlines
    """
    elements = r.split()
    elements = list(filter(strip_line, elements))
    array = []
    while len(elements) > 0:
        row = []
        for i in range(4):
            if i in [0, 3]: # Keep the 'Name' and 'Cover' columns
                row.append(elements.pop(0))
            else: # Pop off the 'Stmts' and 'Miss' columns
                elements.pop(0)
        concatenated_row = '    '.join(row)
        if concatenated_row.startswith('TOTAL') or \
            concatenated_row == 'Name    Cover':
            concatenated_row = '**' + concatenated_row + '**'
        concatenated_row = concatenated_row.replace('__', '\_\_')
        array.append(concatenated_row)
    return '\n'.join(array)


def titled_coverage_report(service_name, coverage_report):
    return "# " + service_name + " Coverage Report" + "\n\n" + coverage_report


def main(service_name, coverage_report, github_repo, github_issue_number, session):
    if github_issue_number == '0':
        return
    coverage_report = format_coverage_report(coverage_report)
    comment_id = get_comment(
        service_name=service_name,
        github_repo=github_repo,
        github_issue_number=github_issue_number,
        session=session)
    if not comment_id:
        create_comment(
            service_name=service_name,
            github_repo=github_repo,
            github_issue_number=github_issue_number,
            coverage_report=coverage_report,
            session=session
        )
    else:
        update_comment(
            service_name=service_name,
            github_repo=github_repo,
            comment_id=comment_id,
            coverage_report=coverage_report,
            session=session)


if __name__=="__main__":
    with github_session(sys.argv[3]) as session:
        main(
            service_name=sys.argv[1],
            coverage_report=sys.argv[2],
            github_repo=sys.argv[4],
            github_issue_number=sys.argv[5],
            session=session
        )
