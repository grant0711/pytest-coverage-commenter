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
import requests

def get_headers(github_token):
    return {
        'Authorization': f'Bearer {github_token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }

def github_session(github_token):
    s = requests.Session()
    s.headers.update(get_headers(github_token))
    return s

def get_comment(service_name, github_repo, github_token, github_issue_number, session=None):
    with session or github_session(github_token) as s:
        response = s.get(
            url=f"https://api.github.com/repos/{github_repo}/issues/{github_issue_number}/comments"
        )
        print(response)
        print(response.data)
        return response

def create_comment(service_name, github_repo, github_token, github_issue_number, coverage_report, session=None):
    return

def update_comment(service_name, github_repo, github_token, github_issue_number, coverage_report, session=None):
    return