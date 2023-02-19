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
        response_json = response.json()
        for comment in response_json:
            if comment.get('body', '').startswith(service_name + ' Coverage Report') and \
                comment.get('user', {}).get('login') == 'github-actions[bot]':
                return comment['id']
        return None

"""
{
    'url': 'https://api.github.com/repos/grant0711/talk_to_me/issues/comments/1435741756',
    'html_url': 'https://github.com/grant0711/talk_to_me/pull/2#issuecomment-1435741756',
    'issue_url': 'https://api.github.com/repos/grant0711/talk_to_me/issues/2',
    'id': 1435741756,
    'node_id': 'IC_kwDOIrj9T85Vk648',
    'user': {
        'login': 'grant0711',
        'id': 47125463,
        'node_id': 'MDQ6VXNlcjQ3MTI1NDYz',
        'avatar_url': 'https://avatars.githubusercontent.com/u/47125463?v=4',
        'gravatar_id': '',
        'url': 'https://api.github.com/users/grant0711',
        'html_url': 'https://github.com/grant0711',
        'followers_url': 'https://api.github.com/users/grant0711/followers',
        'following_url': 'https://api.github.com/users/grant0711/following{/other_user}',
        'gists_url': 'https://api.github.com/users/grant0711/gists{/gist_id}',
        'starred_url': 'https://api.github.com/users/grant0711/starred{/owner}{/repo}',
        'subscriptions_url': 'https://api.github.com/users/grant0711/subscriptions',
        'organizations_url': 'https://api.github.com/users/grant0711/orgs',
        'repos_url': 'https://api.github.com/users/grant0711/repos',
        'events_url': 'https://api.github.com/users/grant0711/events{/privacy}',
        'received_events_url': 'https://api.github.com/users/grant0711/received_events',
        'type': 'User',
        'site_admin': False
    },
    'created_at': '2023-02-18T19:04:49Z',
    'updated_at': '2023-02-18T19:04:49Z',
    'author_association': 'OWNER',
    'body': 'Test comment',
    'reactions': {
        'url': 'https://api.github.com/repos/grant0711/talk_to_me/issues/comments/1435741756/reactions',
        'total_count': 0,
        '+1': 0,
        '-1': 0,
        'laugh': 0,
        'hooray': 0,
        'confused': 0,
        'heart': 0,
        'rocket': 0,
        'eyes': 0
    },
    'performed_via_github_app': None
}
"""

def create_comment(service_name, github_repo, github_token, github_issue_number, coverage_report, session=None):
    with session or github_session(github_token) as s:
        s.headers.update({'Content-Type': 'application/json'})
        response = s.post(
            url=f"https://api.github.com/repos/{github_repo}/issues/{github_issue_number}/comments",
            data=json.dumps({
                "body": service_name + " Coverage Report" + "\n\n" + coverage_report
            })
        )
        response_json = response.json()
        print(response_json)
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
        response_json = response.json()
        print(response_json)
    return