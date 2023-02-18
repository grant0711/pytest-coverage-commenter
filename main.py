import sys

import requests

if __name__=="__main__":
    print('hello')
    print(sys.argv)


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
