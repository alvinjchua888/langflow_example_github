# Usage Guide - Multi-Agent Chat System

This guide provides detailed instructions on how to use the Multi-Agent Chat System.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Agent Capabilities](#agent-capabilities)
3. [Using the Streamlit Interface](#using-the-streamlit-interface)
4. [Example Queries](#example-queries)
5. [Understanding Agent Routing](#understanding-agent-routing)
6. [Troubleshooting](#troubleshooting)

## Quick Start

### 1. Setup Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 2. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### 3. Run the Demo (Optional)

```bash
python demo.py
```

This will showcase each agent's capabilities with example queries.

## Agent Capabilities

### 🎯 Supervisor Agent
- **Purpose**: Intelligently routes queries to the most appropriate specialized agent
- **How it works**: Analyzes the user's query using GPT-3.5 and determines which agent should handle it
- **Routing logic**: Based on query intent, keywords, and context

### 🔢 Math Agent
- **Purpose**: Performs mathematical computations and solves numerical problems
- **Capabilities**:
  - Basic arithmetic (+, -, *, /)
  - Advanced operations (sqrt, sin, cos, tan, log, exp)
  - Mathematical constants (pi, e)
  - Expression evaluation
- **Example queries**:
  - "Calculate 15% of 250"
  - "What is the square root of 144?"
  - "Solve: (25 + 75) * 2 / 10"
  - "Calculate sin(pi/2)"

### 💾 SQL Agent
- **Purpose**: Converts natural language into SQL queries
- **Capabilities**:
  - Query generation from natural language
  - Basic syntax validation
  - Assumes standard table structures
- **Example queries**:
  - "Get all users who registered after January 1, 2023"
  - "Create a query to find the top 10 products by sales"
  - "Write SQL to join customers and orders tables"
  - "Query to count active users by month"

### 🔍 Search Agent
- **Purpose**: Finds information using Google search (or LLM knowledge if SerpAPI is not configured)
- **Capabilities**:
  - Web search integration (requires SerpAPI key)
  - Information retrieval
  - Answer summarization
- **Example queries**:
  - "What is the capital of France?"
  - "Who won the Nobel Prize in Physics 2023?"
  - "What is artificial intelligence?"
  - "Explain quantum computing"

## Using the Streamlit Interface

### Chat Interface

1. **Enter your query** in the chat input at the bottom of the screen
2. **Press Enter** to submit your query
3. **View the response** along with agent details

### Agent Details

Each response includes:
- **Agent Used**: Which specialized agent handled the query
- **Reasoning**: Why the supervisor chose that agent
- **Confidence**: The supervisor's confidence level in the routing decision

### Sidebar Features

- **API Key Status**: Shows which API keys are configured
- **Clear Chat History**: Button to reset the conversation
- **Example Queries**: Sample queries for each agent type

### Tips for Best Results

1. **Be specific**: Clear, well-formed questions get better results
2. **One task at a time**: Focus each query on a single task
3. **Check agent details**: Review the routing decision to understand how your query was interpreted
4. **Use appropriate language**: 
   - For math: Use clear mathematical expressions
   - For SQL: Describe the data and operation you want
   - For search: Ask specific, factual questions

## Example Queries

### Math Examples

```
"Calculate the area of a circle with radius 5"
"What is 23.5 * 18.2?"
"Convert 100 Fahrenheit to Celsius using the formula: (F - 32) * 5/9"
"Find the value of: sqrt(169) + log(100)"
```

### SQL Examples

```
"Get all products where price is greater than 100"
"Create a query to find users who haven't logged in for 30 days"
"Write SQL to calculate total revenue by product category"
"Query to find duplicate email addresses in the users table"
```

### Search Examples

```
"What are the latest developments in renewable energy?"
"Explain the concept of machine learning"
"What is the population of Tokyo?"
"Who is the current CEO of Microsoft?"
```

### Mixed Examples (Testing Supervisor Routing)

```
"Calculate 25% tip on a $87.50 bill"  → Math Agent
"Find products with stock less than 10" → SQL Agent
"What is climate change?"              → Search Agent
```

## Understanding Agent Routing

The Supervisor Agent uses GPT-3.5 to analyze queries and make routing decisions. Here's how it determines which agent to use:

### Math Agent Selection
- Keywords: calculate, compute, solve, equation, percentage, multiply, divide
- Intent: Numerical computation or mathematical problem-solving
- Example: "Calculate 15 * 23"

### SQL Agent Selection
- Keywords: query, database, table, select, join, SQL, data
- Intent: Database querying or SQL generation
- Example: "Create a query to get all users"

### Search Agent Selection
- Keywords: what is, who is, when, where, why, search, find information
- Intent: Information retrieval or knowledge questions
- Example: "What is the capital of France?"

### Fallback Behavior
If the supervisor is uncertain, it defaults to the **Search Agent** as it has the broadest applicability.

## Troubleshooting

### Common Issues

#### 1. "OPENAI_API_KEY not found" error
**Solution**: 
- Create a `.env` file from `.env.example`
- Add your OpenAI API key: `OPENAI_API_KEY=sk-...`
- Restart the Streamlit application

#### 2. Search Agent shows "SERPAPI_API_KEY not configured" note
**Solution**: 
- This is optional; the agent will use LLM knowledge instead
- To enable live search, get a free key from https://serpapi.com/
- Add it to `.env`: `SERPAPI_API_KEY=your_key_here`

#### 3. Agent gives unexpected results
**Possible causes**:
- Query is ambiguous or unclear
- Wrong agent was selected
- API rate limits or connectivity issues

**Solutions**:
- Rephrase your query more specifically
- Check the "Agent Details" to see routing decision
- Verify your internet connection and API keys

#### 4. Streamlit app won't start
**Solution**:
- Check if port 8501 is already in use
- Try: `streamlit run app.py --server.port 8502`
- Verify all dependencies are installed: `pip install -r requirements.txt`

#### 5. Math Agent calculation errors
**Solution**:
- Ensure mathematical expression uses valid operators
- Use parentheses for complex expressions
- For special functions, use Python syntax: sqrt(x), sin(x), etc.

### Getting Help

If you encounter issues not covered here:
1. Check the console/terminal for error messages
2. Review the README.md for setup instructions
3. Verify all dependencies are correctly installed
4. Check that your Python version is 3.8 or higher

## Advanced Usage

### Customizing Agents

Each agent can be customized by modifying its corresponding file in the `agents/` directory:
- `supervisor_agent.py` - Routing logic
- `math_agent.py` - Mathematical operations
- `sql_agent.py` - SQL generation rules
- `search_agent.py` - Search and summarization

### Adding New Agents

1. Create a new agent class in `agents/`
2. Update `agents/__init__.py` to export the new agent
3. Add the agent to `app.py` initialization
4. Update the supervisor agent to recognize the new agent type

### Configuring the LLM

By default, the system uses GPT-3.5-turbo. To change this:
1. Open `app.py`
2. Modify the `initialize_agents()` function
3. Change the model parameter: `ChatOpenAI(temperature=0, model="your-model")`

## Best Practices

1. **Start with simple queries** to understand how each agent works
2. **Review agent details** to learn how the system routes queries
3. **Use clear, specific language** for better results
4. **Keep API keys secure** - never commit them to version control
5. **Monitor API usage** to avoid unexpected costs
6. **Clear chat history** periodically for better performance

## Next Steps

- Experiment with different query types
- Try combining multiple agents for complex workflows
- Explore the source code to understand the implementation
- Consider extending the system with additional specialized agents

---

For more information, see the main [README.md](README.md) file.
