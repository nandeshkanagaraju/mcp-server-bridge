import pytest
from core.security.query_validator import is_select_only

# A list of valid SELECT queries that should be allowed
valid_select_queries = [
    "SELECT * FROM employees;",
    "SELECT first_name, salary FROM employees WHERE dept_id = 5 ORDER BY salary DESC;",
    "select emp_id from employees limit 10",
    "   SELECT * FROM departments   ", # with whitespace
]

# A list of invalid or malicious queries that MUST be blocked
invalid_queries = [
    "UPDATE employees SET salary = 120000 WHERE emp_id = 1;",
    "DELETE FROM employees WHERE emp_id = 1;",
    "DROP TABLE employees;",
    "INSERT INTO employees (first_name) VALUES ('Mallory');",
    "SELECT * FROM employees; DROP TABLE departments;", # SQL Injection attempt
    "", # Empty query
    "-- This is just a comment", # Comment only
    "TRUNCATE TABLE employees;",
]

@pytest.mark.parametrize("query", valid_select_queries)
def test_is_select_only_allows_valid_queries(query):
    """
    Tests that the validator correctly identifies and allows various safe SELECT queries.
    """
    assert is_select_only(query) is True

@pytest.mark.parametrize("query", invalid_queries)
def test_is_select_only_blocks_invalid_queries(query):
    """
    Tests that the validator correctly blocks non-SELECT statements and malicious queries.
    """
    assert is_select_only(query) is False

def test_is_select_only_blocks_multiple_statements():
    """
    Specifically tests the critical security case of chained SQL commands.
    """
    malicious_query = "SELECT * FROM users; UPDATE passwords SET pass = '123' WHERE user = 'admin';"
    assert is_select_only(malicious_query) is False