#!/bin/sh -l

echo "service-name = $1"
echo "service-directory = $2"
echo "github_token = $3"

curl --request GET \
    --url "https://api.github.com/octocat" \
    --header "Authorization: Bearer $3"

