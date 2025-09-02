FORBIDDEN_KEYWORDS = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]

def is_safe_query(query: str) -> bool:
    """
    Returns True if the query is safe (only SELECT), False otherwise.
    """
    query_upper = query.strip().upper()
    # Must start with SELECT
    if not query_upper.startswith("SELECT"):
        return False
    # Must not contain forbidden keywords
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in query_upper:
            return False
    return True