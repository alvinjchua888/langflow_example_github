# Copilot Instructions for Multi-Agent Chat System

## Architecture Overview

This is a **supervisor-worker multi-agent system** built with LangChain, OpenAI GPT-3.5, and Streamlit. The supervisor agent routes queries to specialized agents (Math, SQL, Search) based on LLM-powered intent analysis. All agents share a single `ChatOpenAI(temperature=0, model="gpt-3.5-turbo")` instance initialized in [app.py](../app.py).

**Key Data Flow:** `Streamlit UI → SupervisorAgent.route_request() → specialized agent.run() → response → UI with routing metadata`

## Critical Development Patterns

### Agent Structure
All agents in [agents/](../agents/) follow this pattern:
- `__init__(self, llm=None)`: Accept optional shared LLM, default to new ChatOpenAI instance
- `run(self, query: str) -> str`: Main execution method that returns string responses
- Use `ChatPromptTemplate` from `langchain_core.prompts` for all LLM interactions
- Use LCEL (LangChain Expression Language) with pipe operator: `chain = prompt | self.llm`

Example from [math_agent.py](../agents/math_agent.py):
```python
chain = prompt | self.llm
response = chain.invoke({"query": query})
```

### Supervisor Routing Pattern
[supervisor_agent.py](../agents/supervisor_agent.py) uses JSON-structured prompts to return routing decisions:
```python
{
    "primary_agent": "math|sql|search",
    "reasoning": "explanation",
    "confidence": "high|medium|low"
}
```
The supervisor handles JSON extraction from markdown code blocks and defaults to "search" agent on errors.

### Safe Math Evaluation
[math_agent.py](../agents/math_agent.py) uses restricted `eval()` with sanitized namespace:
- `safe_dict` with `__builtins__={}` to disable built-in functions
- Only allows math functions: `sqrt`, `sin`, `cos`, `tan`, `log`, `exp`, `pi`, `e`
- Regex pre-filter: `r'[^0-9+\-*/().sqrt()sincotanlgexpi\s]'`

### SQL Query Validation
[sql_agent.py](../agents/sql_agent.py) performs basic validation:
- Checks for SQL keywords (SELECT, INSERT, etc.)
- Validates balanced parentheses
- Strips markdown code blocks: `if "```sql" in sql_query`
- Assumes standard table schemas (users, products, orders, customers)

## Running & Testing

```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add OPENAI_API_KEY (required), SERPAPI_API_KEY (optional)

# Run app
streamlit run app.py  # Launches on http://localhost:8501

# Test agents
python test_agents.py       # Import and routing tests
python verify_installation.py  # Full system validation
python demo.py             # Interactive demo of all agents
```

**Note:** Search agent gracefully degrades without SERPAPI_API_KEY, falling back to LLM knowledge with a user-facing note.

## Streamlit Integration

[app.py](../app.py) uses specific Streamlit patterns:
- `@st.cache_resource` decorator on `initialize_agents()` to share LLM across sessions
- Session state keys: `messages` (list of chat history), `agents_initialized` (bool)
- Agent metadata in message dict: `{"role", "content", "agent", "reasoning", "confidence"}`
- Expanders for agent details: `with st.expander("🔍 Agent Details"):`

## Configuration

[langflow_config.json](../langflow_config.json) documents agent capabilities but is **not actively loaded** by the code. It serves as reference documentation for:
- Agent types and tools
- Routing strategy ("llm_based" with "search" fallback)
- Required environment variables per agent

## Adding New Agents

1. Create `agents/new_agent.py` with `__init__(llm=None)` and `run(query: str) -> str`
2. Export in [agents/__init__.py](../agents/__init__.py): `from .new_agent import NewAgent`
3. Update [supervisor_agent.py](../agents/supervisor_agent.py) `available_agents` dict
4. Initialize in [app.py](../app.py) `initialize_agents()`: `agents["new"] = NewAgent(llm)`
5. Add routing examples to sidebar in [app.py](../app.py)

## Common Pitfalls

- **LLM responses with markdown:** All agents strip `\`\`\`json` and `\`\`\`sql` blocks before parsing
- **Error handling:** Agents return string error messages (e.g., `"Error in Math Agent: ..."`) instead of raising exceptions
- **Temperature=0:** All agents use deterministic mode for consistent outputs
- **No async:** Current implementation is fully synchronous; use `st.spinner("Thinking...")` for UX
- **No persistent storage:** Conversation history is in-memory session state only

## Documentation Structure

- [README.md](../README.md): Installation, features, quick examples
- [QUICKSTART.md](../QUICKSTART.md): 5-minute setup guide
- [USAGE_GUIDE.md](../USAGE_GUIDE.md): Detailed agent capabilities, example queries
- [ARCHITECTURE.md](../ARCHITECTURE.md): Component details, data flow, integration points
- [PROJECT_SUMMARY.md](../PROJECT_SUMMARY.md): Technical overview and statistics
