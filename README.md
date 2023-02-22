# Pytest-coverage-commenter

## Description:

Pytest-coverage-commenter adds a detailed coverage comment to pull requests. This is intended to provide a quick and easy way to assess test coverage during normal development process without requiring additional manually work.

![Alt text](example_comment.png?raw=true "Example Coverage Comment")


## Required input arguments:

### `service-name`

Name of service that is being tested with coverage. This is utilized within the comment and utilized on subsequent workflow runs to find and update the existing comment instead of creating a new one. If omitted, will default to an empty string.

### `github-token`

Github token utilized for authentication. You should pass in secrets.GITHUB_TOKEN. This will already be available within your repository secrets.

### `coverage-report`

The string output of a coverage report run. See example below on how to pass in the output of a coverage report run into this action.

## Optional input arguments:

### `github-repo`

The owner/name of your github repository. This will default to the current repository context, so defining a value for this field is not recommended.

### `github-issue`

The issue number of the pull request. This will default to the current pull request context, so defining a value for this field is not recommended.


## An example of how to use this action in a workflow:

If utilizing within a python monorepo, you may create a github action workflow yaml file for each specific service (i.e. directory). At the top of your yaml file, you can specify the specific paths with which to run the coverage commenter.

### Assuming you have a directory structure as follows:

```
project/
  .github/
    workflows/
      api.yaml
      portal.yaml
  services/
    api/
    portal/
```

### Here is an example api.yaml file:

```
name: API service workflow

on:
  pull_request:
    branches: [ "**" ]
    paths:
      - "services/api/**"
  push:
    branches: [ "main" ]
    paths:
      - "services/api/**"

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
        service-name: 'API'
        coverage-report: ${{ steps.coverage-report.outputs.COVERAGE_REPORT }}
        github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Development

Local development is facilitated by utilizing Docker and docker-compose:

```
docker-compose build coverage_commenter_test
docker-compose up coverage_commenter_test
```

When you bring up this container, pytest-watch will run on any changes made within the project directory.

## Contributions

If you happen to find this a useful action, but desire to see it behave differently, please contribute! I created this action with the goal of learning how to create a custom Github Action via Docker and python, and to have something that I can utilize in other personal projects down the line.

## TODOs

- Format coverage comment in a table within comment body: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-tables
- Calculate total coverage independently of the coverage report, as the total is misleading if --skip-empty or --skip-covered are set to true when generating a coverage report
