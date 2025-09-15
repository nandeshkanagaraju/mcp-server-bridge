from config.logger import logger
from services import llm_service, schema_service
from core.database.query_executor import execute_sql
from core.security.query_validator import is_select_only
# 1. Import the new caching service
from storage.cache import redis_cache

async def run_natural_language_query(question: str, session_id: str):
    """
    Orchestrates the full Text-to-SQL workflow, now with caching.
    """
    logger.info(f"Received NLQ for session '{session_id}': '{question}'")

    # 2. Check the cache first
    cache_key = redis_cache.create_cache_key(question)
    cached_result = await redis_cache.get_from_cache(cache_key)
    if cached_result:
        return cached_result # Return the cached result immediately

    # --- If it's a cache miss, proceed with the normal workflow ---
    
    schema_yaml = await schema_service.get_schema_as_yaml_string()
    if not schema_yaml:
        return {"status": "error", "message": "Could not retrieve database schema."}

    generated_sql = await llm_service.generate_sql_from_prompt(
        question=question,
        schema=schema_yaml,
        session_id=session_id
    )

    if not is_select_only(generated_sql):
        logger.warning(f"Validation failed. LLM generated a non-SELECT query: {generated_sql}")
        return {"status": "error", "message": "Generated query is not a valid SELECT statement."}

    try:
        data = await execute_sql(generated_sql)
        
        # We still update conversation history for context
        await llm_service.update_conversation_history(
            session_id=session_id,
            user_question=question,
            assistant_sql=generated_sql,
            data_result=data
        )

        final_result = {
            "status": "success",
            "generated_sql": generated_sql,
            "data": data
        }
        
        # 3. Save the new result to the cache before returning
        await redis_cache.set_to_cache(cache_key, final_result)
        
        return final_result

    except Exception as e:
        logger.error(f"Error executing the generated SQL: {e}")
        return {
            "status": "error",
            "generated_sql": generated_sql,
            "message": f"An error occurred while executing the query: {e}"
        }