#!/bin/sh -l

#echo "service-name = $1"
#echo "coverage-report = $2"
#echo "github_token = $3"

python main.py $1 $2 $3

#curl --request GET \
#    --url "https://api.github.com/octocat" \
#    --header "Authorization: Bearer $3" \
#    --header "Accept: application/vnd.github+json" \
#    --header "X-GitHub-Api-Version: 2022-11-28"
