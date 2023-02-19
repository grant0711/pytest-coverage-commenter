from ..action import main

TEST_CR_INPUT = "Name Stmts Miss Cover ---------------------------------------- tests/conftest.py 4 1 75% __init__.py 0 0 100% main.py 2 0 100% tests/__init__.py 0 0 100% tests/test_main.py 3 0 100% ---------------------------------------- TOTAL 9 1 89%"
EXPECTED_CR_OUTPUT = "Name Cover\n\ntests/conftest.py 75%\n__init__.py 100%\nmain.py 100%\ntests/__init__.py 100%\ntests/test_main.py 100%\n\nTOTAL 89%"

def test_format_coverage_report():
    assert main.format_coverage_report(TEST_CR_INPUT) == EXPECTED_CR_OUTPUT
