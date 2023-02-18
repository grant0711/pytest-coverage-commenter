# Pytest-coverage-commenter

## Description:

Pytest-coverage-commenter adds a detailed coverage comment to pull requests. This is intended to provide a quick and easy way to assess test coverage during normal development process without requiring additional manually work.

## Required input arguments:

## `service-name`

Name of service that is being tested with coverage. This is utilized within the comment and utilized on subsequent workflow runs to find and update the existing comment instead of creating a new one. If omitted, will default to an empty string.

## `github-token`

Github token utilized for authentication. You should pass in secrets.GITHUB_TOKEN. This will already be available within your repository secrets.

## `github-repo`

The owner/name of your github repository. This will default to the current repository context, so defining a value for this field is not required.

## `github-issue`

The issue number of the pull request. This will default to the current pull request context, so defining a value for this field is not required.


## An example of how to use this action in a workflow:

If utilizing within a python monorepo, you may create a github action workflow yaml file for each specific service (i.e. directory). At the top of your yaml file, you can specify the specific paths with which to run the coverage commenter.

See the example below for an example github actions yaml file.


```
name: Name of your Github Action Workflow

on:
  pull_request:
    branches: [ "**" ]
    paths:
      - "path/to/your/service/**"
  push:
    branches: [ "main" ]
    paths:
      - "path/to/your/service/**"

jobs:
  build:
    
    ... Build your test container here first

    - name: Test with pytest and generate coverage report
      id: coverage-report
      run: |
        coverage run -m pytest
        report="$(coverage report --sort=cover)"
        echo "COVERAGE_REPORT="$report"" >> $GITHUB_OUTPUT
    
    - name: Run coverage commenter
      uses: grant0711/pytest-coverage-commenter@v2
      with:
        service-name: 'Your Service Name'
        coverage-report: ${{ steps.coverage-report.outputs.COVERAGE_REPORT }}
        github-token: ${{ secrets.GITHUB_TOKEN }}
```

