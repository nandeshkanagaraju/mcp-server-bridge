# Universal MCP: An Intelligent Database Gateway

A universal Model Context Protocol (MCP) server that provides secure, intelligent database access. It supports both direct SQL execution and natural language queries (Text-to-SQL) powered by Large Language Models (LLMs).

## 🏗️ Architecture

The server architecture now integrates the intelligence layer directly, offering a hybrid approach to data access.

```
┌─────────────────┐    MCP Protocol     ┌──────────────────────────────────┐
│                 │    (HTTP+SSE)       │                                  │
│   MCP Clients   │◄──────────────────►│     Universal MCP Server         │
│ (VSCode, etc.)  │                     │                                  │
└─────────────────┘                     │ ┌──────────────────────────────┐ │
                                        │ │       Intelligence           │ │
┌─────────────────┐    REST API         │ │                                │ │
│                 │                     │ │ • NLP-to-SQL (via REST API)  │ │
│  REST Clients   │◄──────────────────►│ │ • LLM Integration (ChatGPT)  │ │
│ (Web Apps, etc.)│                     │ │ • Conversation Memory        │ │
└─────────────────┘                     │ │ • SQL Generation & Validation│ │
                                        │ └──────────────────────────────┘ │
                                        │ ┌──────────────────────────────┐ │
                                        │ │    Core Services & Tools     │ │
                                        │ │                              │ │
                                        │ │ • Schema Management          │ │
                                        │ │ • Secure Query Executor      │ │
                                        │ │ • Multi-DB Support           │ │
                                        │ └───────────────┬──────────────┘ │
                                        └─────────────────│────────────────┘
                                                          │
                                                          ▼
                                        ┌──────────────────────────────────┐
                                        │         Physical Databases       │
                                        │ (PostgreSQL, MySQL, SQLite, etc.)│
                                        └──────────────────────────────────┘
```

## 🎯 Purpose

Universal MCP serves as a hybrid database gateway that:

*   Provides a secure REST API for converting natural language questions into SQL queries.
*   Manages conversation history for contextual understanding.
*   Provides secure, validated SQL execution via the traditional MCP protocol.
*   Generates database schema YAML for tool configuration and LLM context.
*   Supports multiple database types through a flexible adapter pattern.

## ✨ New Feature: Natural Language Queries (Text-to-SQL)

The server now includes a powerful REST API endpoint that leverages ChatGPT to translate plain English into SQL.

*   **Conversational Memory:** Use a `session_id` to ask follow-up questions. The server remembers the context of your conversation.
*   **Secure by Design:** All LLM-generated queries are passed through a security validator that ensures only safe `SELECT` statements are executed.
*   **Easy Integration:** Any client that can make an HTTP request can now interact with your database using natural language.

### Example Usage

```bash
# Ask an initial question
curl -X POST "http://127.0.0.1:8000/api/v1/query/natural-language" \
-H "Content-Type: application/json" \
-d '{
    "question": "Show me the top 3 highest paid employees",
    "session_id": "my_chat_session_1"
}'

# Ask a follow-up question in the same session
curl -X POST "http://127.0.0.1:8000/api/v1/query/natural-language" \
-H "Content-Type: application/json" \
-d '{
    "question": "of those, who was hired most recently?",
    "session_id": "my_chat_session_1"
}'
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
git clone <repository-url>
cd universal-mcp

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your database credentials and OpenAI API key
nano .env
```

**Important:** You must add your `OPENAI_API_KEY` to the `.env` file.

### 3. Start the Server

```bash
# The server provides both the MCP tools and the REST API
uvicorn api.main:app --reload --port 8000
```

## 🔧 Available Tools & API

### Natural Language API

| Endpoint                       | Method | Description                                                |
| :----------------------------- | :----- | :--------------------------------------------------------- |
| `/api/v1/query/natural-language` | `POST`   | Converts a natural language question to a SQL query and executes it. |

### Traditional MCP Tools

| Tool             | Description                                   |
| :--------------- | :-------------------------------------------- |
| `execute_query`    | Execute validated SQL queries safely.         |
| `get_schema`       | Retrieve complete database schema.            |
| `list_tables`      | Get list of available tables.                 |
| `describe_table`   | Get detailed table structure.                 |
| `get_table_data`   | Retrieve paginated data from tables.          |
| `validate_query`   | Validate SQL syntax and security.             |

### Using Pagination

The `get_table_data` tool supports pagination to handle large tables efficiently. You can use the `page` and `page_size` parameters to request specific chunks of data.

```python
# This is a hypothetical client call to the tool
result = await run_get_table_data(
    table_name="employees",
    page=2,         # Fetch the second page
    page_size=50    # With 50 rows per page
)
```

## 📊 Monitoring & Observability

### How to Access Logs

There are two primary ways to see the system's logs:

1.  **Real-time Console Output (Live View)** All logs are streamed directly to the terminal where the server is running. This is the best way to watch requests as they happen.
2.  **Persistent Log File (For Review)** The server also writes all logs to a file named `mcp_server.log` in the root of the project directory. This is useful for reviewing past events. You can access it with standard terminal commands:

```bash
# View the entire log file
cat mcp_server.log

# View the file page by page (good for long files)
less mcp_server.log

# Watch the file for new logs in real-time
tail -f mcp_server.log
```

### Log Configuration

You can control the verbosity of the logs by changing the `LOG_LEVEL` variable in your `.env` file. Supported levels include `DEBUG`, `INFO`, `WARNING`, and `ERROR`.

```
# .env file
LOG_LEVEL="INFO" # Change to "DEBUG" for more detailed output
```

## 📁 Project Structure (Highlights)

```
universal-mcp/
├── mcp_server.log               # Main log file
├── config/
│   └── settings.py              # Loads configs, including OPENAI_API_KEY
├── core/
│   ├── security/
│   │   └── query_validator.py   # Includes security check for LLM queries
│   └── mcp/
│       └── tools/
│           ├── natural_language_query.py # New tool for orchestrating NLQ
│           └── ...
├── api/
│   ├── main.py                  # Main FastAPI application
│   └── query_routes.py          # Defines the /query/natural-language endpoint
├── services/
│   ├── ll_service.py           # Handles all interaction with OpenAI API
│   ├── query_service.py         # Business logic for queries
│   └── schema_service.py        # Generates schema for LLM context
└── ...
```

## 🔒 Security Features

*   **LLM Query Validation:** All generated SQL is validated to ensure it is `SELECT`-only and contains no malicious chained commands.
*   **SQL Injection Prevention:** Parameterized query validation for direct SQL execution.
*   **Query Sanitization:** Clean and validate SQL statements.
*   **Rate Limiting:** Prevent abuse and resource exhaustion.
*   **Secure Credential Management:** Keys and passwords loaded from `.env`.

## 🗄️ Supported Databases

| Database   | Status       | Adapter                |
| :--------- | :----------- | :--------------------- |
| PostgreSQL | ✅ Supported | `postgresql_adapter.py`  |
| MySQL      | ✅ Supported | `mysql_adapter.py`       |
| SQLite     | ✅ Supported | `sqlite_adapter.py`      |
| Oracle     | 🚧 Planned   | -                      |
| SQL Server | 🚧 Planned   | -                      |

## 🐳 Deployment

### Docker

```bash
# Build and run
docker-compose up -d

# Health check
curl http://localhost:8000/health
```

## 🧪 Development

### Running Tests

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/
```

