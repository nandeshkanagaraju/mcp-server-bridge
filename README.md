# Universal MCP

A universal Model Context Protocol (MCP) server that provides secure database access and schema introspection via HTTP+SSE transport. Designed as a pure data access layer that works with intelligent MCP clients handling NLP-to-SQL conversion.

## 🏗️ Architecture

```
┌─────────────────┐    MCP Protocol     ┌──────────────────────┐
│                 │    (HTTP+SSE)       │                      │
│   MCP Clients   │◄──────────────────►│  Universal MCP       │
│                 │                     │     Server           │
│ • Claude Desktop│                     │                      │
│ • VSCode        │                     │ • Schema Reader      │
│ • Custom Apps   │                     │ • Query Executor     │
│ • Web Clients   │                     │ • Security Layer     │
└─────────────────┘                     │ • Multi-DB Support   │
                                        └──────────┬───────────┘
┌─────────────────┐                                │
│  Intelligence   │                                │
│                 │                                ▼
│ • NLP Processing│                     ┌──────────────────────┐
│ • LLM Integration│                     │                      │
│ • Context Memory│                     │    Databases         │
│ • SQL Generation│                     │                      │
└─────────────────┘                     │ • PostgreSQL         │
                                        │ • MySQL              │
    (Client Side)                       │ • SQLite             │
                                        │ • Oracle (future)    │
                                        └──────────────────────┘
```

## 🎯 Purpose

Universal MCP serves as a **universal database gateway** that:
- Provides secure, validated SQL execution via MCP protocol
- Generates database schema YAML for MCP tool configuration
- Supports multiple database types through adapter pattern
- Streams large query results via HTTP+SSE transport
- Handles security, validation, and connection management

**Note**: This server does NOT include NLP/LLM processing. Clients are responsible for natural language understanding and SQL generation.

## 📁 Project Structure

```
universal-mcp/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── docker-compose.yml               # Container orchestration
├── .env.example                      # Environment configuration template
├── .gitignore                        # Git ignore rules
│
├── config/                           # Configuration Management
│   ├── __init__.py
│   ├── settings.py                   # App settings and environment variables
│   ├── database.py                   # Database connection configurations
│   └── mcp_config.py                 # MCP server and transport settings
│
├── core/                             # Core Business Logic
│   ├── __init__.py
│   ├── database/                     # Database Layer
│   │   ├── __init__.py
│   │   ├── connection_manager.py     # Connection pooling and management
│   │   ├── query_executor.py         # Safe SQL execution with validation
│   │   ├── health_monitor.py         # Database health monitoring
│   │   └── adapters/                 # Database-specific implementations
│   │       ├── __init__.py
│   │       ├── base_adapter.py       # Abstract base adapter
│   │       ├── postgresql_adapter.py # PostgreSQL implementation
│   │       ├── mysql_adapter.py      # MySQL implementation
│   │       └── sqlite_adapter.py     # SQLite implementation
│   │
│   ├── schema/                       # Schema Management
│   │   ├── __init__.py
│   │   ├── schema_reader.py          # Extract database schema metadata
│   │   ├── metadata_extractor.py     # Parse table/column information
│   │   ├── yaml_generator.py         # Generate YAML for FastMCP
│   │   └── schema_cache.py           # Cache schema for performance
│   │
│   ├── security/                     # Security Layer
│   │   ├── __init__.py
│   │   ├── query_validator.py        # SQL injection prevention
│   │   ├── sql_sanitizer.py          # Query sanitization
│   │   └── rate_limiter.py           # Rate limiting implementation
│   │
│   └── mcp/                          # MCP Protocol Implementation
│       ├── __init__.py
│       ├── server.py                 # Main MCP server
│       ├── transport/                # Transport Layer
│       │   ├── __init__.py
│       │   ├── http_sse_transport.py # HTTP+SSE transport
│       │   └── stdio_transport.py    # STDIO transport (dev)
│       ├── handlers/                 # Protocol Handlers
│       │   ├── __init__.py
│       │   ├── protocol_handler.py   # MCP protocol handling
│       │   └── message_handler.py    # Message processing
│       ├── tools/                    # MCP Tools
│       │   ├── __init__.py
│       │   ├── execute_query.py      # Execute SQL queries
│       │   ├── get_schema.py         # Retrieve schema information
│       │   ├── list_tables.py        # List available tables
│       │   ├── describe_table.py     # Table structure details
│       │   ├── get_table_data.py     # Sample table data
│       │   └── validate_query.py     # Query validation
│       └── resources/                # MCP Resources
│           ├── __init__.py
│           └── schema_resources.py   # Schema resource management
│
├── api/                              # Minimal Health API
│   ├── __init__.py
│   ├── main.py                       # FastAPI app (health only)
│   └── health.py                     # Health check endpoints
│
├── services/                         # Business Logic Services
│   ├── __init__.py
│   ├── schema_service.py             # Schema extraction orchestration
│   ├── query_service.py              # Query execution business logic
│   └── database_service.py           # Database operations coordination
│
├── observability/                    # Monitoring & Logging
│   ├── __init__.py
│   ├── monitoring.py                 # System monitoring setup
│   ├── metrics.py                    # Custom metrics collection
│   ├── health_checks.py              # Health check implementations
│   └── logging_config.py             # Structured logging setup
│
├── storage/                          # Caching & Storage
│   ├── __init__.py
│   ├── cache/                        # Caching Layer
│   │   ├── __init__.py
│   │   ├── redis_cache.py            # Redis caching implementation
│   │   └── memory_cache.py           # In-memory caching
│   └── session/                      # Session Management
│       ├── __init__.py
│       └── context_store.py          # MCP session storage
│
├── schemas/                          # Schema Files
│   ├── generated/                    # Auto-generated YAML schemas
│   │   └── .gitkeep
│   └── templates/                    # Schema templates
│       └── schema_template.yaml      # Base schema template
│
├── tests/                            # Test Suite
│   ├── __init__.py
│   ├── conftest.py                   # Pytest configuration
│   ├── unit/                         # Unit Tests
│   │   ├── __init__.py
│   │   ├── test_schema_reader.py     # Schema reading tests
│   │   ├── test_query_executor.py    # Query execution tests
│   │   ├── test_database_adapters.py # Database adapter tests
│   │   └── test_mcp_tools.py         # MCP tools tests
│   ├── integration/                  # Integration Tests
│   │   ├── __init__.py
│   │   ├── test_mcp_server.py        # MCP server integration
│   │   └── test_database_connections.py # Database integration
│   └── fixtures/                     # Test Data
│       ├── sample_schema.yaml        # Sample schema files
│       └── test_database.sql         # Test database setup
│
├── scripts/                          # Utility Scripts
│   ├── __init__.py
│   ├── setup_database.py             # Database initialization
│   ├── generate_schema.py            # Schema YAML generation
│   ├── start_mcp_server.py           # MCP server startup
│   └── test_mcp_connection.py        # MCP connection testing
│
├── docs/                             # Documentation
│   ├── mcp/
│   │   └── protocol_docs.md          # MCP protocol documentation
│   ├── deployment/
│   │   └── docker_setup.md           # Docker deployment guide
│   └── examples/
│       ├── sample_queries.md         # Example queries and usage
│       └── integration_examples.py   # Integration code examples
│
└── deployment/                       # Deployment Configuration
    ├── docker/                       # Docker Configuration
    │   ├── Dockerfile                # Production Dockerfile
    │   ├── Dockerfile.dev             # Development Dockerfile
    │   └── nginx.conf                # Nginx configuration
    ├── k8s/                          # Kubernetes Manifests
    │   ├── deployment.yaml           # K8s deployment
    │   ├── service.yaml              # K8s service
    │   └── configmap.yaml            # K8s configuration
    └── scripts/                      # Deployment Scripts
        ├── deploy.sh                 # Deployment automation
        └── health_check.sh           # Health check script
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
git clone <repository-url>
cd universal-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Database
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env  # Add your database credentials
```

### 3. Generate Database Schema
```bash
# Generate YAML schema for MCP tools
python scripts/generate_schema.py --database your_database_name
```

### 4. Start MCP Server
```bash
# Start with HTTP+SSE transport
python scripts/start_mcp_server.py --transport http --port 8080

# Optional: Start health API
uvicorn api.main:app --port 8081
```

### 5. Test Connection
```bash
# Test MCP connection
python scripts/test_mcp_connection.py
```

## 🔧 MCP Tools Available

| Tool | Description | Usage |
|------|-------------|-------|
| `execute_query` | Execute validated SQL queries safely | Primary query execution |
| `get_schema` | Retrieve complete database schema | Schema introspection |
| `list_tables` | Get list of available tables | Table discovery |
| `describe_table` | Get detailed table structure | Table metadata |
| `get_table_data` | Retrieve sample data from tables | Data exploration |
| `validate_query` | Validate SQL syntax and security | Query validation |

---

## 📝 Logging & Observability Enhancements

The `logging-tools` feature introduces **centralized structured logging** for all MCP tools and server operations, providing:

- **Automatic logging** for every tool execution (`execute_query`, `get_schema`, `list_tables`, `describe_table`, `get_table_data`, `validate_query`).
- **Info, warning, and error levels** to track success, failures, and exceptions.
- **Query and schema logging** to trace SQL statements and database interactions.
- **Consistent log format** with timestamps, tool names, and execution results.
- **Easy debugging**: Quickly identify which tool or query caused issues.
- **Optional logging test script**: `scripts/test_logging_all.py` validates all tools and generates example logs.

### Example Log Output
2025-09-04 02:31:35,418 | INFO | MCPServer | Executing query: SELECT * FROM employees LIMIT 3;
2025-09-04 02:31:35,522 | INFO | MCPServer | Query successful. Returned 3 rows.
2025-09-04 02:31:35,545 | INFO | MCPServer | Schema fetched: ['assignments', 'departments', 'employees', 'projects']


> Logs are stored in a centralized manner and can be configured via `observability/logging_config.py`.

---

## 🔌 MCP Resources

| Resource | Description | URI Pattern |
|----------|-------------|-------------|
| `schema` | Database schema information | `schema://database/{table_name}` |
| `table` | Table metadata and structure | `table://database/{table_name}` |
| `connection` | Database connection status | `connection://database/status` |

## 🌐 Client Integration

### Connection Example
```python
# MCP client connection
import mcp

client = mcp.Client(transport="http://localhost:8080")
await client.connect()

# Execute query via MCP
result = await client.call_tool("execute_query", {
    "query": "SELECT * FROM employees LIMIT 5",
    "database": "company_db"
})
```

### Supported Transports
- **HTTP+SSE** (Production): `http://localhost:8080`
- **STDIO** (Development): Direct process communication

## 🔒 Security Features

- **SQL Injection Prevention**: Parameterized query validation
- **Query Sanitization**: Clean and validate SQL statements
- **Rate Limiting**: Prevent abuse and resource exhaustion
- **Connection Security**: Secure database credential management
- **Query Timeouts**: Prevent long-running queries
- **Whitelist/Blacklist**: Control allowed SQL operations

## 🗄️ Supported Databases

| Database | Status | Adapter | Notes |
|----------|---------|---------|-------|
| PostgreSQL | ✅ Supported | `postgresql_adapter.py` | Full feature support |
| MySQL | ✅ Supported | `mysql_adapter.py` | Full feature support |
| SQLite | ✅ Supported | `sqlite_adapter.py` | Local development |
| Oracle | 🚧 Planned | - | Future implementation |
| SQL Server | 🚧 Planned | - | Future implementation |

## 📊 Monitoring & Observability

- **Health Checks**: Database connectivity and server status
- **Metrics**: Query execution times, connection pool status
- **Logging**: Structured logging with correlation IDs
- **Monitoring**: Prometheus metrics (optional)

## 🐳 Deployment

### Docker
```bash
# Build and run
docker-compose up -d

# Health check
curl http://localhost:8081/health
```

### Kubernetes
```bash
# Deploy to K8s
kubectl apply -f deployment/k8s/
```

## 🧪 Development

### Running Tests
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# All tests with coverage
pytest --cov=core --cov=services
```

### Code Quality
```bash
# Format code
black .
isort .

# Type checking
mypy core/ services/

# Linting
flake8 core/ services/
```

## 📚 Documentation

- [MCP Protocol Documentation](docs/mcp/protocol_docs.md)
- [Docker Deployment Guide](docs/deployment/docker_setup.md)
- [Integration Examples](docs/examples/integration_examples.py)
- [Sample Queries](docs/examples/sample_queries.md)

