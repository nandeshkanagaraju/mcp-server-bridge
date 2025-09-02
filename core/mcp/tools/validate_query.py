def validate_query(query: str):
    """
    Basic validation: check if query is a SELECT statement
    """
    if not query.strip().lower().startswith("select"):
        return False, "Only SELECT queries are allowed."
    return True, ""
