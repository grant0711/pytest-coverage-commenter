import json
from unittest.mock import patch, Mock

import pytest

from ..action import main

SERVICE_NAME = 'TEST'
COVERAGE_REPORT_RAW = "Name Stmts Miss Cover ---------------------------------------- tests/conftest.py 4 1 75% __init__.py 0 0 100% main.py 2 0 100% tests/__init__.py 0 0 100% tests/test_main.py 3 0 100% ---------------------------------------- TOTAL 9 1 89%"
GITHUB_TOKEN = 'testtoken'
GITHUB_REPO = 'github_repo'
GITHUB_ISSUE_NUMBER = '2'

EXPECTED_CR_OUTPUT_NO_TITLE = "## Name    Cover\ntests/conftest.py    75%\n__init__.py    100%\nmain.py    100%\ntests/__init__.py    100%\ntests/test_main.py    100%\n## TOTAL    89%"
EXPECTED_CR_OUTPUT_WITH_TITLE = "# " + SERVICE_NAME + " Coverage Report\n\n" + EXPECTED_CR_OUTPUT_NO_TITLE


def test_github_session():
    with main.github_session(GITHUB_TOKEN) as session:
        headers = session.headers
        assert headers['Accept'] == 'application/vnd.github+json'
        assert headers['Authorization'] == 'Bearer testtoken'
        assert headers['X-GitHub-Api-Version'] == '2022-11-28'


class ExistingCommentGetCommentResponse():
    def __init__(self):
        self.status_code = 200
    def json(self):
        return [{
            'body': EXPECTED_CR_OUTPUT_WITH_TITLE,
            'user': {
                'login': 'github-actions[bot]'
            },
            'id': 12345
        }]


class NonExistingCommentGetCommentResponse():
    def __init__(self):
        self.status_code = 200
    def json(self):
        return [{
            'body': 'This is a comment from someone else',
            'user': {
                'login': 'test_user'
            },
            'id': 23541
        }]


class SuccessPostPatchResponse():
    def __init__(self):
        self.status_code = 201


class FailurePostPatchResponse():
    def __init__(self):
        self.status_code = 400


def test_get_existing_comment():
    mock_session = Mock()
    mock_session.get = Mock(return_value=ExistingCommentGetCommentResponse())
    comment_id = main.get_comment(
        service_name=SERVICE_NAME,
        github_repo=GITHUB_REPO,
        github_issue_number=GITHUB_ISSUE_NUMBER,
        session=mock_session
    )
    assert comment_id == 12345
    mock_session.get.assert_called_once_with(
        url=f'https://api.github.com/repos/{GITHUB_REPO}/issues/{GITHUB_ISSUE_NUMBER}/comments'
    )


def test_get_non_existing_comment():
    mock_session = Mock()
    mock_session.get = Mock(return_value=NonExistingCommentGetCommentResponse())
    comment_id = main.get_comment(
        service_name=SERVICE_NAME,
        github_repo=GITHUB_REPO,
        github_issue_number=GITHUB_ISSUE_NUMBER,
        session=mock_session
    )
    assert comment_id == None


def test_create_comment_success():
    mock_session = Mock()
    mock_session.post = Mock(return_value=SuccessPostPatchResponse())
    main.create_comment(
        service_name=SERVICE_NAME,
        github_repo=GITHUB_REPO,
        github_issue_number=GITHUB_ISSUE_NUMBER,
        coverage_report=EXPECTED_CR_OUTPUT_NO_TITLE,
        session=mock_session
    )
    mock_session.post.assert_called_once_with(
        url='https://api.github.com/repos/github_repo/issues/2/comments',
        data=json.dumps({"body": EXPECTED_CR_OUTPUT_WITH_TITLE})
    )


def test_create_comment_failure():
    mock_session = Mock()
    mock_session.post = Mock(return_value=FailurePostPatchResponse())
    
    with pytest.raises(Exception):
        main.create_comment(
            service_name=SERVICE_NAME,
            github_repo=GITHUB_REPO,
            github_issue_number=GITHUB_ISSUE_NUMBER,
            coverage_report=EXPECTED_CR_OUTPUT_NO_TITLE,
            session=mock_session
        )


def test_update_comment_success():
    mock_session = Mock()
    mock_session.patch = Mock(return_value=SuccessPostPatchResponse())
    main.update_comment(
        service_name=SERVICE_NAME,
        github_repo=GITHUB_REPO,
        comment_id=12345,
        coverage_report=EXPECTED_CR_OUTPUT_NO_TITLE,
        session=mock_session
    )
    mock_session.patch.assert_called_once_with(
        url='https://api.github.com/repos/github_repo/issues/comments/12345',
        data=json.dumps({"body": EXPECTED_CR_OUTPUT_WITH_TITLE})
    )


def test_format_coverage_report():
    assert main.format_coverage_report(COVERAGE_REPORT_RAW) == EXPECTED_CR_OUTPUT_NO_TITLE


def test_titled_coverage_report():
    assert main.titled_coverage_report(SERVICE_NAME, EXPECTED_CR_OUTPUT_NO_TITLE) == EXPECTED_CR_OUTPUT_WITH_TITLE


def test_main_creates_new_comment():
    mock_session = Mock()
    mock_session.get = Mock(return_value=NonExistingCommentGetCommentResponse())
    mock_session.post = Mock(return_value=SuccessPostPatchResponse())
    mock_session.patch = Mock()
    main.main(
        service_name=SERVICE_NAME,
        coverage_report=COVERAGE_REPORT_RAW,
        github_repo=GITHUB_REPO,
        github_issue_number=GITHUB_ISSUE_NUMBER,
        session=mock_session
    )
    mock_session.get.assert_called_once()
    mock_session.post.assert_called_once()
    mock_session.patch.assert_not_called()


def test_main_updates_existing_comment():
    mock_session = Mock()
    mock_session.get = Mock(return_value=ExistingCommentGetCommentResponse())
    mock_session.post = Mock()
    mock_session.patch = Mock(return_value=SuccessPostPatchResponse())
    main.main(
        service_name=SERVICE_NAME,
        coverage_report=COVERAGE_REPORT_RAW,
        github_repo=GITHUB_REPO,
        github_issue_number=GITHUB_ISSUE_NUMBER,
        session=mock_session
    )
    mock_session.get.assert_called_once()
    mock_session.post.assert_not_called()
    mock_session.patch.assert_called_once()
