# Universal MCP: An Intelligent Database Gateway

Universal MCP is an intelligent database gateway that provides secure, intelligent database access. It supports both direct SQL execution via the MCP protocol and **natural language queries (Text-to-SQL)** through a REST API powered by OpenAI's GPT models.

## Description

Universal MCP serves as a **hybrid database gateway** that:
- Provides a secure REST API for converting **natural language questions into SQL queries**.
- Manages conversation history for contextual, multi-turn questions.
- Provides secure, validated SQL execution via the traditional MCP protocol.
- Generates database schema YAML for tool configuration and LLM context.
- Supports multiple database types through a flexible adapter pattern.

## Features

### Natural Language Queries (Text-to-SQL)

The server now includes a powerful REST API and an interactive terminal client that leverages ChatGPT to translate plain English into SQL.

- **Conversational Memory:** Use the interactive chat client or a `session_id` to ask follow-up questions. The server remembers the context of your conversation using a persistent file-based session store.
- **Secure by Design:** All LLM-generated queries are passed through a security validator that ensures only safe `SELECT` statements are executed.
- **Interactive Terminal Client:** A rich, user-friendly terminal interface (`scripts/chat.py`) allows you to have a full conversation with your database.

## Architecture

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
│  REST Clients   │◄───────────────────►│ │ • LLM Integration (ChatGPT)  │ │
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

## Quick Start (Local Setup)

This guide will help you run the application directly on your local machine (macOS/Linux).

### 1. Prerequisites
- Python 3.11+
- A running local MySQL server.

### 2. Setup Environment
```bash
git clone <repository-url>
cd universal-mcp

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your local database credentials and OpenAI API key
nano .env
```
**Important:** You must add your `OPENAI_API_KEY` and ensure your `DB_HOST`, `DB_USER`, and `DB_PASSWORD` match your local MySQL setup.

### 4. Initialize the Database
This script will create the necessary tables and populate them with sample data in your local MySQL database.

```bash
python scripts/setup_database.py
```

### 5. Start the Server
This command starts the FastAPI server which provides the REST API.

```bash
# Leave this terminal running
uvicorn api.main:app --reload --port 8000
```

### 6. Chat with Your Database
Open a new terminal window and start the interactive chat client.

```bash
# Make sure your virtual environment is activated
source venv/bin/activate

# Run the chat script
python scripts/chat.py
```

## Available Tools & API

### Natural Language API

| Endpoint                       | Method | Description                                                |
| :----------------------------- | :----- | :--------------------------------------------------------- |
| `/api/v1/query/natural-language` | `POST`   | Converts a natural language question to a SQL query and executes it. |

### Traditional MCP Tools

| Tool            | Description                                  |
| :-------------- | :------------------------------------------- |
| `execute_query`   | Execute validated SQL queries safely.        |
| `get_schema`      | Retrieve complete database schema.           |
| `list_tables`     | Get list of available tables.                |
| `describe_table`  | Get detailed table structure.                |
| `get_table_data`  | Retrieve paginated data from tables.         |
| `validate_query`  | Validate SQL syntax and security.            |

## Project Structure (Highlights)

```
universal-mcp/
├── config/
│   └── settings.py              # Loads configs, including OPENAI_API_KEY
├── core/
│   ├── security/
│   │   └── query_validator.py   # Includes security check for LLM queries
│   └── mcp/
│       └── tools/
│           └── natural_language_query.py # New tool for orchestrating NLQ
├── api/
│   ├── main.py                  # Main FastAPI application
│   └── query_routes.py          # Defines the /query/natural-language endpoint
├── services/
│   ├── llm_service.py           # Handles all interaction with OpenAI API
│   └── schema_service.py        # Generates schema for LLM context
├── storage/
│   └── session/
│       └── context_store.py     # Manages file-based session memory
├── scripts/
│   ├── setup_database.py        # Initializes the local database
│   └── chat.py                  # The interactive terminal chat client
└── tests/
    ├── unit/
    │   └── test_query_validator.py # Unit test for security
    └── integration/
        └── test_nlq_endpoint.py  # Integration test for the API
```

## Security Features

- **LLM Query Validation:** All generated SQL is validated to ensure it is `SELECT`-only and contains no malicious chained commands.
- **SQL Injection Prevention:** Parameterized query validation for direct SQL execution.
- **Query Sanitization:** Clean and validate SQL statements.
- **Rate Limiting:** Prevent abuse and resource exhaustion.
- **Secure Credential Management:** Keys and passwords loaded from `.env` file`.
