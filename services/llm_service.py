import openai
import json
from config.settings import settings
from config.logger import logger
# Import our new persistent file-based context store
from storage.session import context_store

# --- These functions now use the file store ---
def get_conversation_history(session_id: str) -> list:
    """Retrieves conversation history for a given session from a file."""
    return context_store.get_history(session_id)

def update_conversation_history(session_id: str, user_question: str, assistant_sql: str, data_result: list):
    """
    Updates the conversation history file with the latest exchange.
    """
    history = get_conversation_history(session_id)
    history.append({"role": "user", "content": user_question})

    data_summary = f"The previous query returned {len(data_result)} rows. Here is a sample of the data (up to 2 rows): {json.dumps(data_result[:2], default=str)}" if data_result else "The previous query returned no results."
    
    assistant_content = f"""I generated the following SQL:\n```sql\n{assistant_sql}\n```\nAnd here is a summary of the result:\n{data_summary}"""
    history.append({"role": "assistant", "content": assistant_content.strip()})

    context_store.set_history(session_id, history)

# --- The rest of the file remains the same ---
async def generate_sql_from_prompt(question: str, schema: str, session_id: str) -> str:
    """
    Generates a safe SELECT SQL query from a natural language question using OpenAI.
    """
    client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    history = get_conversation_history(session_id) # This now reads from a file
    
    system_prompt = f"""You are an expert SQL analyst. Your task is to convert natural language questions into SQL queries for a database with the following schema provided in YAML format:
---
{schema}
---
Based on the conversation history (which includes the user's questions, the SQL you generated, and a summary of the results), generate the appropriate SQL query for the user's latest question.

Rules:
1. You MUST only generate a single, valid `SELECT` statement.
2. Do NOT generate any `UPDATE`, `DELETE`, `INSERT`, `DROP`, or any other non-SELECT statements.
3. Do not add any explanation, notes, or markdown formatting (like ```sql) around the SQL query.
4. Your entire response should only be the raw SQL query.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        *history,
        {"role": "user", "content": question}
    ]

    try:
        logger.info(f"Generating SQL for session {session_id}...")
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.0,
            n=1
        )
        sql_query = response.choices[0].message.content.strip()
        
        logger.info(f"Generated SQL: {sql_query}")
        
        if sql_query.startswith("```sql"):
            sql_query = sql_query[6:]
        if sql_query.endswith("```"):
            sql_query = sql_query[:-3]
            
        return sql_query.strip()
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        return "SELECT 'Error generating query';"