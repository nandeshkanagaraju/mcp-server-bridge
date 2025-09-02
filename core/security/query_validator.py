import sqlparse

def validate_sql(sql: str) -> bool:
    """
    Allow only safe SELECT queries.
    Blocks DROP, DELETE, UPDATE, INSERT.
    """
    parsed = sqlparse.parse(sql)
    if not parsed:
        return False

    stmt = parsed[0]
    first_token = stmt.token_first(skip_cm=True)
    if first_token and first_token.value.upper() == "SELECT":
        return True
    return False
