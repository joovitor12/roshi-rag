# Memory Integration in Roshi RAG Chatbot

## Overview

The chatbot now supports persistent memory to maintain conversation context between sessions. Two storage options are available:

1. **In-Memory Storage** (MemorySaver) - For testing and development
2. **PostgreSQL** (AsyncPostgresSaver) - For production with real persistence

## Setup

### Prerequisites

1. **Ollama** must be running:
   ```bash
   ollama serve
   ```

2. **PostgreSQL** (only for persistent memory):
   ```bash
   # Create database
   createdb roshi_rag_memory
   ```

### Event Loop Configuration (Windows)

For PostgreSQL compatibility on Windows, the event loop is automatically configured in test files and main.py:

```python
import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```

## Usage

### 1. Test with In-Memory Storage

```bash
poetry run python -m test.test_llm_stream
```

This test uses `MemorySaver` which maintains memory only during the session.

### 2. Test with PostgreSQL

```bash
poetry run python -m test.test_postgres_memory
```

This test uses `AsyncPostgresSaver` for real persistence in PostgreSQL.

### 3. FastAPI API

```bash
poetry run uvicorn main:app --reload
```

The API uses PostgreSQL by default, with automatic fallback to in-memory storage if PostgreSQL is not available.

## Architecture

### LLMService

The `LLMService` class has been updated to support both memory types:

```python
# In-memory storage (for testing)
llm_service = LLMService(use_postgres=False)

# PostgreSQL (for production)
llm_service = LLMService(use_postgres=True)
```

### Asynchronous Agents

All agents have been converted to asynchronous functions for compatibility with the asynchronous checkpointer:

- `planner_node` (supervisor_agent.py)
- `chatbot_node` (chat_agent.py)
- `joke_node` (joke_agent.py)
- `synthesizer_node` (synthesizer_agent.py)

### Memory Flow

1. **Initialization**: The service initializes the appropriate checkpointer
2. **State Recovery**: Fetches conversation history using `thread_id`
3. **Processing**: Adds new message to existing history
4. **Persistence**: The checkpointer automatically saves the new state

## Testing Memory

### Basic Test

1. Start a conversation:
   ```
   You: Hi, my name is João and I'm 25 years old
   ```

2. Continue the conversation:
   ```
   You: What's my name?
   AI: Your name is João.
   ```

3. Test new conversation:
   ```
   You: new
   You: What's my name?
   AI: I don't know your name. Could you please tell me?
   ```

### Persistence Test (PostgreSQL)

1. Start a conversation and note the ID
2. Close the program
3. Restart and use the same conversation_id
4. Verify that context was maintained

## Database Configuration

### Connection String

```python
conn_string = "postgresql://postgres:1234@localhost:5432/roshi_rag_memory"
```

### Tables

LangGraph automatically creates the necessary tables:
- `checkpoints` - Conversation states
- `checkpoint_blobs` - Binary checkpoint data

## Troubleshooting

### Error: "All connection attempts failed"
- Check if Ollama is running: `ollama serve`

### Error: "Synchronous calls to AsyncPostgresSaver"
- Make sure all agents are `async` functions
- Use `await` for graph calls with PostgreSQL

### Error: "ProactorEventLoop"
- The event loop is automatically configured for Windows
- Make sure the configuration is at the beginning of the file

### Automatic Fallback

If PostgreSQL fails, the system automatically uses in-memory storage:

```
❌ Failed to initialize PostgreSQL memory: [error]
🔄 Falling back to in-memory storage
```

## Next Steps

1. **Environment Variable Configuration**: Move settings to `.env`
2. **Connection Pooling**: Optimize PostgreSQL connections
3. **Memory Cleanup**: Implement automatic cleanup of old conversations
4. **Metrics**: Add memory usage monitoring
