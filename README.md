Pytest-coverage-commenter

Description:

Pytest-coverage-commenter adds a detailed coverage comment to pull requests. This is intended to provide a quick and easy way to assess test coverage during normal development process without requiring additional manually work.

Required input and output arguments:

service-name = Name of service (parent folder) that is being tested with coverage. This is utilized within the comment and utilized on subsequent workflow runs to find and update the existing comment instead of creating a new one. If omitted, will default to an empty string.

service-directory = Parent directory of service to be tested with coverage. This is utilized in case of a monorepo setup where only a certain service is to be tested instead of the whole repo.

Secrets the action uses:

TBD

Environment variables the action uses:

TBD

An example of how to use this action in a workflow:

TBD