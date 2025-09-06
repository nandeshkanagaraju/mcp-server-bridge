import openai
from config.settings import settings
from config.logger import logger

# In-memory store for conversation history. Key: session_id, Value: list of messages.
conversation_cache = {}

# Initialize the asynchronous OpenAI client
try:
    client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    client = None

def get_conversation_history(session_id: str) -> list:
    """Retrieves or creates a conversation history for a given session."""
    if session_id not in conversation_cache:
        conversation_cache[session_id] = []
    return conversation_cache[session_id]

def update_conversation_history(session_id: str, user_question: str, assistant_sql: str):
    """Updates the conversation history with the latest exchange."""
    history = get_conversation_history(session_id)
    history.append({"role": "user", "content": user_question})
    # We store the assistant's response (the SQL) for context in the next turn
    history.append({"role": "assistant", "content": assistant_sql})

async def generate_sql_from_prompt(question: str, schema: str, session_id: str) -> str:
    """
    Generates a safe SELECT SQL query from a natural language question using OpenAI.
    """
    if not client:
        return "SELECT 'Error: OpenAI client not initialized';"

    history = get_conversation_history(session_id)
    
    system_prompt = f"""You are an expert SQL analyst. Your task is to convert natural language questions into SQL queries for a database with the following schema provided in YAML format:
---
{schema}
---
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
            model="gpt-4o",  # Using a modern, capable model
            messages=messages,
            temperature=0.0, # Low temperature for deterministic SQL generation
            n=1
        )
        sql_query = response.choices[0].message.content.strip()
        
        update_conversation_history(session_id, question, sql_query)
        
        logger.info(f"Generated SQL: {sql_query}")
        return sql_query
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        return "SELECT 'Error generating query';"