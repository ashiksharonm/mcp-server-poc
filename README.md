# MCP Server POC - Agent Tool Gateway

A production-ready implementation of a (mock) Model Context Protocol server. This project simulates an Agent Tool Gateway that exposes standardized tools to LLM agents, complete with validation, logging, retries, and an evaluation harness.

## Features

- **Tool Gateway**: Exposes tools structured with Pydantic schemas.
- **Agent Simulation**: Mock LLM orchestration (extensible to real OpenAI).
- **Batteries Included**: 3 implemented tools (Ticket Search, KB Lookup, Safe DB Query).
- **Safety**: SQL injection prevention for DB queries.
- **Observability**: Structured logging and latency tracking.
- **Robustness**: Retries used for flaky external services (simulated in KB lookup).
- **Evals**: Built-in regression testing harness.

## Quick Start

### 1. Local Setup

Requires Python 3.11+

```bash
# Clone and install dependencies
pip install . 
# OR use existing requirements
pip install fastapi uvicorn pydantic-settings httpx tenacity loguru aiosqlite

# Set up environment
cp .env.example .env

# Run server
uvicorn app.main:app --reload
```

Server will be running at `http://localhost:8000`.
Docs available at `http://localhost:8000/docs`.

### 2. Docker Setup

```bash
docker-compose up --build
```

## Tools

| Tool Name | Description | Input |
|-----------|-------------|-------|
| `ticket_search` | Search tickets by keyword | `{"query": "string"}` |
| `kb_lookup` | Lookup topics in Knowledge Base | `{"topic": "string"}` |
| `db_query` | Run SAFE SQL (SELECT only) | `{"sql": "string"}` |

## Running Tests

```bash
# Unit & Integration Tests
pytest

# Evaluation Harness (requires server running)
# Start server first in one terminal: uvicorn app.main:app
python evals/run_evals.py
```

## Project Structure

- `app/`: Core application code.
- `data/`: SQLite database and seed scripts.
- `evals/`: Golden prompts and verification scripts.
- `tests/`: Pytest suite.

## API Usage Examples

**List Tools:**
```bash
curl http://localhost:8000/tools
```

**Run Agent:**
```bash
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{"query": "Find the high priority tickets"}'
```
