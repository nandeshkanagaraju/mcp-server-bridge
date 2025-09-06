from config.logger import logger
from services import llm_service, schema_service
from core.database.query_executor import execute_sql
from core.security.query_validator import is_select_only # Assuming this exists from our plan

async def run_natural_language_query(question: str, session_id: str):
    """
    Orchestrates the full Text-to-SQL workflow.
    This is an 'Available Function/Tool' in your architecture.
    """
    logger.info(f"Received natural language query for session '{session_id}': '{question}'")

    # 1. Get database schema for context [from Schema Management]
    schema_yaml = await schema_service.get_schema_as_yaml_string()
    if not schema_yaml:
        return {"status": "error", "message": "Could not retrieve database schema."}

    # 2. Call LLM service to generate SQL
    generated_sql = await llm_service.generate_sql_from_prompt(
        question=question,
        schema=schema_yaml,
        session_id=session_id
    )

    # 3. Security Validation [using Query Validator]
    if not is_select_only(generated_sql):
        logger.warning(f"Validation failed. LLM generated a non-SELECT query: {generated_sql}")
        return {"status": "error", "message": "Generated query is not a valid SELECT statement."}

    # 4. Execute the safe query [using Query Executor]
    logger.info(f"Executing validated query: {generated_sql}")
    try:
        data = await execute_sql(generated_sql)
        # 5. Format the result [using Result Formatter principles]
        return {
            "status": "success",
            "generated_sql": generated_sql,
            "data": data
        }
    except Exception as e:
        logger.error(f"Error executing the generated SQL: {e}")
        return {
            "status": "error",
            "generated_sql": generated_sql,
            "message": f"An error occurred while executing the query: {e}"
        }