# Multi-Agent Chat System with LangChain and Streamlit

A sophisticated multi-agent system built with LangChain, LangFlow concepts, and Streamlit that intelligently routes user queries to specialized agents.

## 🌟 Features

- **Intelligent Routing**: A supervisor agent automatically analyzes queries and routes them to the most appropriate specialized agent
- **Math Agent**: Performs mathematical calculations and solves numerical problems
- **SQL Agent**: Converts natural language descriptions into SQL queries
- **Search Agent**: Finds information from Google using SerpAPI
- **Interactive Chat Interface**: Built with Streamlit for an intuitive user experience
- **Conversation History**: Maintains chat history throughout the session

## 🏗️ Architecture

The system uses a supervisor-worker pattern:

```
User Query → Supervisor Agent → [Math Agent | SQL Agent | Search Agent] → Response
```

1. **Supervisor Agent**: Analyzes the user's query and determines which specialized agent should handle it
2. **Specialized Agents**: Execute the task using their specific tools and capabilities
3. **Response**: Returns the result to the user through the chat interface

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (required)
- SerpAPI key (optional, for search functionality)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/alvinjchua888/langflow_example_github.git
cd langflow_example_github
```

2. **Create a virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# Required:
OPENAI_API_KEY=your_openai_api_key_here

# Optional (for search functionality):
SERPAPI_API_KEY=your_serpapi_key_here
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 💡 Usage Examples

### Math Queries
- "Calculate 15% of 250"
- "What is the square root of 144?"
- "Solve: (25 + 75) * 2 / 10"

### SQL Queries
- "Get all users who registered after 2023"
- "Create a query to find the top 10 products by sales"
- "Write SQL to join customers and orders tables"

### Search Queries
- "What is the weather in Paris today?"
- "Latest news about AI developments"
- "Who won the Nobel Prize in Physics 2023?"

## 📁 Project Structure

```
langflow_example_github/
├── agents/
│   ├── __init__.py
│   ├── supervisor_agent.py    # Routes queries to appropriate agents
│   ├── math_agent.py          # Handles mathematical computations
│   ├── sql_agent.py           # Generates SQL queries
│   └── search_agent.py        # Performs Google searches
├── app.py                     # Main Streamlit application
├── langflow_config.json       # Langflow configuration
├── requirements.txt           # Python dependencies
├── .env.example              # Example environment variables
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🛠️ Technology Stack

- **LangChain**: Framework for building LLM-powered applications
- **Streamlit**: Web application framework for the chat interface
- **OpenAI GPT-3.5**: Language model for agent reasoning and responses
- **SerpAPI**: Google search integration
- **Python**: Core programming language

## 🔧 Configuration

The `langflow_config.json` file contains the configuration for all agents and their capabilities. This follows Langflow concepts for agent orchestration.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found" error
- Make sure you've created a `.env` file in the project root
- Ensure your OpenAI API key is properly set in the `.env` file
- Restart the Streamlit application after adding the key

### "SERPAPI_API_KEY not found" warning
- This is optional; the search agent will show an error if used without it
- Get a free API key from https://serpapi.com/
- Add it to your `.env` file

### Agent not responding or slow responses
- Check your internet connection
- Verify your API keys are valid
- OpenAI API may have rate limits or service issues

## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub.
