# Text-to-SQL Agent

A natural language to SQL query agent powered by LangChain and Claude Sonnet 4.5. Ask questions about your database in plain English and get accurate SQL queries and results.

## Features

- Natural language to SQL query conversion
- Automatic query validation and error correction
- Support for complex queries (JOINs, aggregations, subqueries)
- LangSmith integration for tracing and debugging
- Interactive tutorial notebook included

## Demo Database

Uses the [Chinook database](https://github.com/lerocha/chinook-database) - a sample database representing a digital media store with tables for artists, albums, tracks, customers, invoices, and more.

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/))
- (Optional) LangSmith API key for tracing ([sign up here](https://smith.langchain.com/))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/kevinbfrank/text2sqlagent.git
cd text2sqlagent
```

2. Create a virtual environment and install dependencies:
```bash
# Using uv (recommended)
uv venv --python 3.11
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Or using standard pip
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Required in `.env`:
```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Optional for LangSmith tracing:
```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=text2sql-agent
```

## Usage

### Using the Agent in Code

```python
from agent import create_sql_agent

# Create the agent
agent = create_sql_agent()

# Ask a question
result = agent.invoke({
    "messages": [{"role": "user", "content": "What are the top 5 best-selling artists?"}]
})

print(result["messages"][-1].content)
```

### Interactive Tutorial

Explore the agent capabilities with the included Jupyter notebook:

```bash
jupyter notebook tutorial.ipynb
```

The tutorial includes:
- Step-by-step agent construction
- 8+ example queries
- LangSmith tracing setup
- Database schema reference

## Example Queries

The agent can handle a wide variety of SQL queries:

**Simple queries:**
- "How many customers are from Canada?"
- "List all genres in the database"

**Aggregations:**
- "What is the total revenue by country?"
- "Which artist has the most albums?"

**Complex JOINs:**
- "What are the top 5 best-selling tracks?"
- "Show me all albums by AC/DC"

**Business analytics:**
- "Which employee has generated the most sales revenue?"
- "What's the average track length by genre?"

## How It Works

The agent uses LangChain's `create_agent` with the following workflow:

1. **Discover** - Lists available tables in the database
2. **Inspect** - Retrieves schema for relevant tables (with sample rows)
3. **Generate** - Creates a SQL query using Claude Sonnet 4.5
4. **Validate** - Double-checks the query for syntax and safety
5. **Execute** - Runs the query against the database
6. **Retry** - If errors occur, automatically rewrites and retries
7. **Format** - Returns results in a readable format

## Architecture

```
User Question
     ↓
Claude Sonnet 4.5 (LLM)
     ↓
SQL Toolkit (Tools)
     ├─ list_tables
     ├─ get_schema
     ├─ query_checker
     └─ execute_query
     ↓
SQLite Database (Chinook)
     ↓
Formatted Answer
```

## Safety Features

- **Read-only access**: Only SELECT queries are allowed
- **No DML statements**: Cannot INSERT, UPDATE, DELETE, or DROP
- **Query validation**: All queries are validated before execution
- **Automatic error recovery**: Failed queries are rewritten and retried
- **Result limiting**: Queries are limited to 5 results by default (configurable)
- **Sample data only**: Schema inspection shows only 3 sample rows per table

## LangSmith Integration

When configured, every query is automatically traced in LangSmith. You can view:
- Complete execution trace with all tool calls
- Token usage and costs
- Query execution time
- Generated SQL queries
- Error messages and retry attempts

![LangSmith Trace Example](text2sql-LangSmithTraceView.png)

View traces at: https://smith.langchain.com/

## Configuration

Key configuration options in `agent.py`:

```python
# Limit sample rows shown in schema
db = SQLDatabase.from_uri(
    "sqlite:///chinook.db",
    sample_rows_in_table_info=3  # Adjust as needed
)

# Default result limit (in system prompt)
system_prompt=SYSTEM_PROMPT.format(
    dialect=db.dialect,
    top_k=5  # Adjust as needed
)
```

## Project Structure

```
text2sqlagent/
├── agent.py              # Core agent implementation
├── test_agent.py         # Interactive CLI for testing
├── tutorial.ipynb        # Jupyter tutorial notebook
├── chinook.db           # Sample SQLite database (gitignored)
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Requirements

- langchain >= 1.2.3
- langchain-anthropic >= 1.3.1
- langchain-community >= 0.3.0
- langgraph >= 1.0.6
- sqlalchemy >= 2.0.0
- python-dotenv >= 1.0.0

See `requirements.txt` for complete list.

## License

MIT

## Acknowledgments

- Built with [LangChain](https://www.langchain.com/)
- Powered by [Claude Sonnet 4.5](https://www.anthropic.com/claude)
- Uses the [Chinook Database](https://github.com/lerocha/chinook-database)
- Tracing via [LangSmith](https://smith.langchain.com/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
