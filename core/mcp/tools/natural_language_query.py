from config.logger import logger
from services import llm_service, schema_service
from core.database.query_executor import execute_sql
from core.security.query_validator import is_select_only

async def run_natural_language_query(question: str, session_id: str):
    """Orchestrates the full Text-to-SQL workflow."""
    logger.info(f"Received NLQ for session '{session_id}': '{question}'")

    schema_yaml = await schema_service.get_schema_as_yaml_string()
    if not schema_yaml:
        return {"status": "error", "message": "Could not retrieve database schema."}

    generated_sql = await llm_service.generate_sql_from_prompt(
        question=question,
        schema=schema_yaml,
        session_id=session_id
    )

    if not is_select_only(generated_sql):
        return {"status": "error", "message": "Generated query is not a valid SELECT statement."}

    try:
        data = await execute_sql(generated_sql)
        
        # This call is now SYNCHRONOUS (no 'await')
        llm_service.update_conversation_history(
            session_id=session_id,
            user_question=question,
            assistant_sql=generated_sql,
            data_result=data
        )

        return { "status": "success", "generated_sql": generated_sql, "data": data }
    except Exception as e:
        return { "status": "error", "generated_sql": generated_sql, "message": f"An error occurred: {e}" }