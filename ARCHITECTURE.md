# Architecture Documentation

## System Overview

The Multi-Agent Chat System is built using a **supervisor-worker pattern** where a central supervisor agent intelligently routes user queries to specialized worker agents.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Streamlit UI                            │
│                      (Chat Interface)                           │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          │ User Query
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Supervisor Agent                             │
│                   (GPT-3.5 powered)                             │
│                                                                 │
│  • Analyzes query intent                                        │
│  • Determines best agent                                        │
│  • Routes to specialized agent                                  │
└──────────────┬──────────────┬──────────────┬───────────────────┘
               │              │              │
      ┌────────▼─────┐  ┌────▼──────┐  ┌───▼──────────┐
      │ Math Agent   │  │ SQL Agent │  │ Search Agent │
      │              │  │           │  │              │
      │ • Calculates │  │ • Parses  │  │ • Searches   │
      │ • Evaluates  │  │ • Generates│ │ • Summarizes │
      │ • Solves     │  │ • Validates│ │ • Retrieves  │
      └──────┬───────┘  └─────┬─────┘  └──────┬───────┘
             │                │               │
             └────────────────┴───────────────┘
                              │
                              │ Response
                              ▼
                     ┌─────────────────┐
                     │  Streamlit UI   │
                     │  (Display)      │
                     └─────────────────┘
```

## Component Details

### 1. Streamlit UI Layer (`app.py`)

**Responsibilities:**
- Present chat interface to users
- Manage conversation history
- Display agent routing information
- Handle user authentication and API key validation

**Key Features:**
- Real-time chat interface
- Agent detail expansion panels
- API key status indicators
- Chat history management

**Technologies:**
- Streamlit for UI
- Session state for conversation management

### 2. Supervisor Agent (`agents/supervisor_agent.py`)

**Responsibilities:**
- Receive and analyze user queries
- Determine query intent and type
- Select the most appropriate specialized agent
- Provide routing reasoning and confidence scores

**Routing Logic:**
```python
Query → LLM Analysis → Intent Classification → Agent Selection
```

**Decision Factors:**
- Keywords in query
- Query structure and syntax
- Contextual understanding
- Domain-specific patterns

**Output Format:**
```json
{
  "primary_agent": "agent_name",
  "reasoning": "explanation",
  "confidence": "high/medium/low"
}
```

### 3. Math Agent (`agents/math_agent.py`)

**Responsibilities:**
- Parse mathematical expressions
- Perform calculations safely
- Handle various mathematical functions
- Format numerical results

**Capabilities:**
- Basic arithmetic operations
- Advanced functions (sqrt, trig, log)
- Expression evaluation
- Safe code execution

**Architecture:**
```
Query → Expression Extraction → Safe Evaluation → Result Formatting
```

**Safety Features:**
- Sandboxed evaluation environment
- Limited function namespace
- Input sanitization
- Error handling

### 4. SQL Agent (`agents/sql_agent.py`)

**Responsibilities:**
- Parse natural language requests
- Generate SQL queries
- Validate query syntax
- Provide query explanations

**Capabilities:**
- SELECT query generation
- JOIN operations
- WHERE clause construction
- GROUP BY and ORDER BY
- Basic syntax validation

**Architecture:**
```
Query → Intent Parsing → SQL Generation → Validation → Formatting
```

**Query Generation Process:**
1. Extract data requirements
2. Identify table and column references
3. Construct appropriate SQL statements
4. Validate syntax
5. Format with code blocks

### 5. Search Agent (`agents/search_agent.py`)

**Responsibilities:**
- Execute web searches (with SerpAPI)
- Retrieve relevant information
- Summarize search results
- Provide sourced answers

**Capabilities:**
- Google search integration
- Result summarization
- Information extraction
- Fallback to LLM knowledge

**Architecture:**
```
Query → Search Execution → Result Processing → Summarization → Response
```

**Search Flow:**
1. Check for SerpAPI availability
2. Execute search if available
3. Process and filter results
4. Summarize key information
5. Format response with citations

## Data Flow

### Complete Request-Response Cycle

```
1. User Input
   ↓
2. Streamlit captures query
   ↓
3. Supervisor Agent receives query
   ↓
4. LLM analyzes intent
   ↓
5. Routing decision made
   ↓
6. Selected agent processes query
   ↓
7. Agent generates response
   ↓
8. Response returned to UI
   ↓
9. Display with agent details
   ↓
10. Update conversation history
```

## Integration Points

### LangChain Integration

The system uses LangChain framework for:
- **LLM Management**: Unified interface to OpenAI models
- **Prompt Templates**: Structured prompts for each agent
- **Chain Composition**: LCEL (LangChain Expression Language) for pipeline
- **Utilities**: SerpAPI wrapper for search functionality

### OpenAI Integration

All agents use OpenAI's GPT-3.5-turbo model:
- **Temperature**: 0 (deterministic responses)
- **Model**: gpt-3.5-turbo
- **API Version**: Latest

### External APIs

1. **OpenAI API** (Required)
   - Used by: All agents
   - Purpose: Language understanding and generation

2. **SerpAPI** (Optional)
   - Used by: Search Agent
   - Purpose: Google search results
   - Fallback: LLM knowledge base

## Configuration

### Environment Variables

```env
OPENAI_API_KEY=<required>     # OpenAI API access
SERPAPI_API_KEY=<optional>    # Google Search access
```

### Agent Configuration (`langflow_config.json`)

```json
{
  "agents": {
    "supervisor": {
      "model": "gpt-3.5-turbo",
      "temperature": 0
    },
    "math": {
      "model": "gpt-3.5-turbo",
      "temperature": 0,
      "tools": ["Calculator"]
    },
    "sql": {
      "model": "gpt-3.5-turbo",
      "temperature": 0,
      "tools": ["SQLGenerator", "SQLValidator"]
    },
    "search": {
      "model": "gpt-3.5-turbo",
      "temperature": 0,
      "tools": ["GoogleSearch", "Summarizer"]
    }
  }
}
```

## Error Handling

### Error Flow

```
Error Occurs
   ↓
Try-Catch at Agent Level
   ↓
Error Message Formatting
   ↓
Return to UI
   ↓
Display User-Friendly Message
```

### Error Types

1. **API Errors**: Authentication, rate limits, connectivity
2. **Validation Errors**: Invalid input, malformed queries
3. **Processing Errors**: Calculation failures, generation issues
4. **System Errors**: Missing dependencies, configuration issues

## Scalability Considerations

### Current Design
- Single user session
- Synchronous processing
- In-memory state

### Future Enhancements
1. **Multi-user Support**: Session management per user
2. **Async Processing**: Non-blocking agent execution
3. **Caching**: Store common query results
4. **Database Integration**: Persistent conversation history
5. **Agent Pool**: Load balancing across agent instances

## Security Considerations

### Current Implementation
- API keys via environment variables
- Safe mathematical expression evaluation
- No direct code execution
- Input sanitization

### Best Practices
- Never commit API keys to repository
- Use environment variables for sensitive data
- Validate all user inputs
- Limit agent capabilities to necessary functions
- Regular dependency updates

## Performance Characteristics

### Typical Response Times
- **Supervisor Routing**: 1-2 seconds
- **Math Agent**: 1-3 seconds
- **SQL Agent**: 2-4 seconds
- **Search Agent**: 3-5 seconds (with SerpAPI)

### Factors Affecting Performance
- OpenAI API latency
- Query complexity
- Network conditions
- SerpAPI availability

## Testing Strategy

### Test Layers
1. **Unit Tests**: Individual agent functionality
2. **Integration Tests**: Agent communication
3. **End-to-End Tests**: Complete request cycle
4. **Manual Tests**: UI and user experience

### Test Coverage
- Import validation
- Agent initialization
- Routing logic
- Query processing
- Error handling

## Monitoring and Logging

### Current Logging
- Streamlit console output
- Agent operation results
- Error messages

### Recommended Additions
- Request/response logging
- Performance metrics
- Error rate tracking
- API usage monitoring

## Deployment Options

### Local Deployment
```bash
streamlit run app.py
```

### Docker Deployment (Future)
```dockerfile
FROM python:3.11
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

### Cloud Deployment (Future)
- Streamlit Cloud
- Heroku
- AWS/GCP/Azure
- Docker containers

## Dependencies

### Core Dependencies
- `streamlit`: Web UI framework
- `langchain`: LLM framework
- `langchain-openai`: OpenAI integration
- `langchain-community`: Community tools
- `langchain-core`: Core functionality

### Optional Dependencies
- `google-search-results`: SerpAPI integration

## Version History

### v1.0.0 (Current)
- Initial implementation
- Four agent types (supervisor, math, sql, search)
- Streamlit chat interface
- LangChain integration
- Basic error handling

---

For implementation details, see the source code in the `agents/` directory.
For usage instructions, see [USAGE_GUIDE.md](USAGE_GUIDE.md).
