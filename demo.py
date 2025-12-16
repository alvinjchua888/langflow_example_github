"""Demo script to showcase the multi-agent system functionality."""
import os
from dotenv import load_dotenv
from agents import MathAgent, SQLAgent, SearchAgent, SupervisorAgent

# Load environment variables
load_dotenv()

def demo_supervisor():
    """Demo the supervisor agent's routing capabilities."""
    print("=" * 70)
    print("DEMO: Supervisor Agent Routing")
    print("=" * 70)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not set. Please configure it to run this demo.")
        return
    
    supervisor = SupervisorAgent()
    
    test_queries = [
        "Calculate the square root of 144",
        "Create a SQL query to find all users registered in 2023",
        "What is the capital of France?",
        "Solve: 25 * 4 + 10",
        "Generate SQL to get top 10 products by sales",
        "Who won the 2023 Nobel Prize in Physics?"
    ]
    
    print("\nRouting different types of queries:\n")
    
    for query in test_queries:
        print(f"Query: {query}")
        result = supervisor.route_request(query)
        print(f"  → Agent: {result['primary_agent']}")
        print(f"  → Reasoning: {result['reasoning']}")
        print(f"  → Confidence: {result['confidence']}")
        print()

def demo_math_agent():
    """Demo the math agent."""
    print("=" * 70)
    print("DEMO: Math Agent")
    print("=" * 70)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not set. Please configure it to run this demo.")
        return
    
    math_agent = MathAgent()
    
    queries = [
        "What is 15% of 250?",
        "Calculate: (100 + 50) * 2 / 3"
    ]
    
    print("\nMath computations:\n")
    
    for query in queries:
        print(f"Query: {query}")
        result = math_agent.run(query)
        print(f"Answer: {result}\n")

def demo_sql_agent():
    """Demo the SQL agent."""
    print("=" * 70)
    print("DEMO: SQL Agent")
    print("=" * 70)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not set. Please configure it to run this demo.")
        return
    
    sql_agent = SQLAgent()
    
    queries = [
        "Get all users who registered after January 1, 2023",
        "Find the top 5 products by sales"
    ]
    
    print("\nSQL query generation:\n")
    
    for query in queries:
        print(f"Request: {query}")
        result = sql_agent.run(query)
        print(f"{result}\n")

def demo_search_agent():
    """Demo the search agent."""
    print("=" * 70)
    print("DEMO: Search Agent")
    print("=" * 70)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not set. Please configure it to run this demo.")
        return
    
    search_agent = SearchAgent()
    
    queries = [
        "What is artificial intelligence?",
    ]
    
    print("\nSearch queries:\n")
    
    for query in queries:
        print(f"Query: {query}")
        result = search_agent.run(query)
        print(f"Answer: {result}\n")

def main():
    """Run all demos."""
    import sys
    
    # Check for non-interactive mode
    non_interactive = '--non-interactive' in sys.argv or os.getenv('DEMO_NON_INTERACTIVE') == '1'
    
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + "  Multi-Agent System Demo".center(68) + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    print("\n")
    
    if non_interactive:
        print("Running in non-interactive mode\n")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ERROR: OPENAI_API_KEY not found in environment variables.")
        print("\nPlease set your OpenAI API key:")
        print("1. Copy .env.example to .env")
        print("2. Add your OpenAI API key to the .env file")
        print("3. Run this demo again\n")
        return
    
    # Run demos
    try:
        demo_supervisor()
        if not non_interactive:
            input("\nPress Enter to continue to Math Agent demo...")
        print("\n")
        
        demo_math_agent()
        if not non_interactive:
            input("\nPress Enter to continue to SQL Agent demo...")
        print("\n")
        
        demo_sql_agent()
        if not non_interactive:
            input("\nPress Enter to continue to Search Agent demo...")
        print("\n")
        
        demo_search_agent()
        
        print("\n" + "=" * 70)
        print("Demo completed! Run 'streamlit run app.py' to try the chat interface.")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}\n")

if __name__ == "__main__":
    main()
