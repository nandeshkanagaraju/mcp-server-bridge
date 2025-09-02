def list_tables(schema: list):
    """
    Returns all table names as a formatted list
    """
    if not schema:
        return "No tables found."
    return [table for table in schema]
