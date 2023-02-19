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
import json

import requests


def github_session(github_token):
    s = requests.Session()
    s.headers.update({
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    })
    return s

def get_comment(service_name, github_repo, github_token, github_issue_number, session=None):
    with session or github_session(github_token) as s:
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

def create_comment(service_name, github_repo, github_token, github_issue_number, coverage_report, session=None):
    with session or github_session(github_token) as s:
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

def update_comment(service_name, github_repo, github_token, comment_id, coverage_report, session=None):
    with session or github_session(github_token) as s:
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