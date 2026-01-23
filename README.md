# Universal MCP: An Intelligent Database Gateway

Universal MCP is an intelligent database gateway designed to provide secure and intelligent access to various databases. It supports both direct SQL execution via the MCP protocol and natural language queries (Text-to-SQL) through a REST API, leveraging OpenAI's GPT models for advanced natural language processing capabilities.

## 🏗️ Architecture

The server architecture integrates an intelligence layer directly, offering a hybrid approach to data access. This design allows for flexible interaction with physical databases while incorporating advanced AI functionalities.

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

## 🎯 Purpose

Universal MCP functions as a hybrid database gateway with the following core purposes:

*   **Secure REST API**: Provides an interface for converting natural language questions into SQL queries.
*   **Conversation Management**: Manages conversation history to support contextual, multi-turn questions.
*   **Secure SQL Execution**: Offers secure and validated SQL execution via the traditional MCP protocol.
*   **Schema Generation**: Generates database schema YAML for tool configuration and LLM context.
*   **Multi-Database Support**: Supports various database types through a flexible adapter pattern.

## ✨ New Feature: Natural Language Queries (Text-to-SQL)

The server now incorporates a robust REST API and an interactive terminal client that utilizes ChatGPT to translate natural language into SQL queries. Key aspects of this feature include:

*   **Conversational Memory**: The system maintains conversation context using a persistent file-based session store, enabling users to ask follow-up questions.
*   **Secure by Design**: All LLM-generated queries undergo a security validation process, ensuring that only safe `SELECT` statements are executed.
*   **Interactive Terminal Client**: A user-friendly terminal interface (`scripts/chat.py`) facilitates full conversational interaction with the database.

## 🚀 Quick Start (Local Setup)

This guide outlines the steps to run the application directly on a local machine (macOS/Linux).

### 1. Prerequisites

*   Python 3.11+
*   A running local MySQL server (installed via Homebrew or standard installer).

### 2. Local MySQL Setup (macOS via Homebrew)

If you don't have MySQL installed:

```bash
# Install MySQL
brew install mysql

# Start the service
brew services start mysql

# Secure installation (optional but recommended)
mysql_secure_installation
```

### 3. Setup Environment

```bash
git clone <repository-url>
cd universal-mcp

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your local database credentials and OpenAI API key
nano .env
```

**Important**: Ensure `OPENAI_API_KEY` is added and `DB_HOST`, `DB_USER`, and `DB_PASSWORD` match your local MySQL setup.

### 5. Initialize the Database

This script creates necessary tables and populates them with sample data in your local MySQL database.

First, ensure the database and user exist. You can run this command (replace `YOUR_PASSWORD` with the password from your `.env` file):

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS company_db; CREATE USER IF NOT EXISTS 'mcp_server_user'@'localhost' IDENTIFIED BY 'YOUR_PASSWORD'; GRANT ALL PRIVILEGES ON company_db.* TO 'mcp_server_user'@'localhost'; FLUSH PRIVILEGES;"
```

Then, run the setup script to create tables and sample data:

```bash
python -m scripts.setup_database
```

### 6. Start the Server

This command starts the FastAPI server, which provides the REST API.

```bash
# Leave this terminal running
uvicorn api.main:app --reload --port 8000
```

### 7. Chat with Your Database

Open a new terminal window and start the interactive chat client.

```bash
# Make sure your virtual environment is activated
source venv/bin/activate

# Run the chat script
python scripts/chat.py
```

## 🔧 Available Tools & APIs

### Natural Language API

| Endpoint                     | Method | Description                                                    |
| :--------------------------- | :----- | :------------------------------------------------------------- |
| `/api/v1/query/natural-language` | `POST`   | Converts a natural language question to a SQL query and executes it. |

### Traditional MCP Tools

| Tool              | Description                                        |
| :---------------- | :------------------------------------------------- |
| `execute_query`     | Execute validated SQL queries safely.              |
| `get_schema`        | Retrieve complete database schema.                 |
| `list_tables`       | Get list of available tables.                      |
| `describe_table`    | Get detailed table structure.                      |
| `get_table_data`    | Retrieve paginated data from tables.               |
| `validate_query`    | Validate SQL syntax and security.                  |

#### Using Pagination

The `get_table_data` tool supports pagination for efficient handling of large tables. Use the `page` and `page_size` parameters to request specific data chunks.

## 📊 Monitoring & Observability

### How to Access Logs

Logs are crucial for debugging and can be accessed in two ways:

*   **Real-time Console Output**: All logs are streamed directly to the terminal where the `uvicorn` server is running.
*   **Persistent Log File**: The server also writes all logs to `mcp_server.log` in the project's root directory.

```bash
# Watch the log file for new entries in real-time
tail -f mcp_server.log
```

The log verbosity can be controlled via the `LOG_LEVEL` variable in your `.env` file (options: `DEBUG`, `INFO`, `WARNING`, `ERROR`).

## 📁 Project Structure (Highlights)

```
universal-mcp/
├── mcp_server.log              # Main log file
├── config/
│   └── settings.py             # Loads configs, including OPENAI_API_KEY
├── core/
│   ├── security/
│   │   └── query_validator.py  # Security check for LLM queries
│   └── mcp/
│       └── tools/
│           └── natural_language_query.py # Orchestrates NLQ
├── api/
│   ├── main.py                 # Main FastAPI application
│   └── query_routes.py         # Defines the NLQ endpoint
├── services/
│   └── llm_service.py          # Handles all interaction with OpenAI API
├── storage/
│   └── session/
│       └── context_store.py    # Manages file-based session memory
├── scripts/
│   ├── setup_database.py       # Initializes the local database
│   └── chat.py                 # The interactive terminal chat client
└── tests/
    ├── unit/
    │   └── test_query_validator.py
    └── integration/
        └── test_nlq_endpoint.py
```

## 🔒 Security Features

*   **LLM Query Validation**: All generated SQL queries are validated to be `SELECT`-only and free of chained commands.
*   **SQL Injection Prevention**: Parameterized query validation is implemented for direct SQL execution.
*   **Secure Credential Management**: API keys and database passwords are loaded securely from the `.env` file.

## 🧪 Development & Testing

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/
```

