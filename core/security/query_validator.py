import sqlparse
from config.logger import logger

def is_select_only(sql: str) -> bool:
    """
    Parses the SQL query and returns True only if it's a single, valid SELECT statement.
    This is a critical security check for LLM-generated queries.
    """
    if not sql:
        logger.warning("Validation failed: SQL query is empty.")
        return False
    
    try:
        # Split statements to prevent multiple commands (e.g., SELECT ...; DROP TABLE ...)
        parsed_statements = sqlparse.parse(sql)
        
        # We only allow one single statement.
        if len(parsed_statements) > 1:
            logger.warning(f"Validation failed: Multiple SQL statements detected in query '{sql}'")
            return False

        statement = parsed_statements[0]
        
        # Check the type of the single statement
        if statement.get_type() == 'SELECT':
            logger.info("SQL validation successful: Query is a valid SELECT statement.")
            return True
        else:
            logger.warning(f"Validation failed: Query is not a SELECT statement. Type: {statement.get_type()}")
            return False
            
    except Exception as e:
        logger.error(f"An unexpected error occurred during SQL parsing: {e}")
        return False

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
