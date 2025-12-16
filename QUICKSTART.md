# Quick Start Guide

Get up and running with the Multi-Agent Chat System in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- SerpAPI key (optional, for search - [Get one here](https://serpapi.com/))

## Installation Steps

### 1. Clone and Navigate

```bash
git clone https://github.com/alvinjchua888/langflow_example_github.git
cd langflow_example_github
```

### 2. Create Virtual Environment

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your keys
# Use any text editor (nano, vim, notepad, etc.)
nano .env
```

Add your keys:
```env
OPENAI_API_KEY=sk-your-openai-key-here
SERPAPI_API_KEY=your-serpapi-key-here  # Optional
```

### 5. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## First Steps

### Try These Example Queries

**Math:**
```
Calculate 15% of 250
```

**SQL:**
```
Create a query to find all users registered in 2023
```

**Search:**
```
What is artificial intelligence?
```

## Testing

Run the test suite to verify everything works:

```bash
python test_agents.py
```

## Demo Mode

See all agents in action:

```bash
python demo.py
```

Or run without interactive prompts:

```bash
python demo.py --non-interactive
```

## Project Structure

```
├── agents/              # Agent implementations
│   ├── supervisor_agent.py
│   ├── math_agent.py
│   ├── sql_agent.py
│   └── search_agent.py
├── app.py              # Main Streamlit application
├── demo.py             # Demo script
├── test_agents.py      # Test suite
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
└── README.md          # Full documentation
```

## Common Issues

### "OPENAI_API_KEY not found"
**Solution:** Make sure you created `.env` file and added your API key

### Port already in use
**Solution:** Run on a different port:
```bash
streamlit run app.py --server.port 8502
```

### Module not found errors
**Solution:** Make sure you activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Next Steps

- 📖 Read the [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed usage instructions
- 🏗️ Check [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system design
- 💬 Start chatting with the agents!

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review [USAGE_GUIDE.md](USAGE_GUIDE.md) for troubleshooting
- Open an issue on GitHub

## What's Next?

Once you're comfortable with the basics:

1. **Experiment with different queries** to understand agent routing
2. **Review the agent details** in each response to learn how decisions are made
3. **Customize agents** by modifying files in the `agents/` directory
4. **Add new agents** by following the existing patterns

---

**Enjoy using the Multi-Agent Chat System!** 🤖✨
