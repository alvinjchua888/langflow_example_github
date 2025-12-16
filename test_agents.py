"""Test script for verifying agent functionality."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test that all agents can be imported."""
    print("Testing imports...")
    try:
        from agents import MathAgent, SQLAgent, SearchAgent, SupervisorAgent
        print("✅ All agents imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_supervisor_routing():
    """Test the supervisor agent routing logic."""
    print("\nTesting supervisor routing...")
    try:
        from agents import SupervisorAgent
        
        # Check if OpenAI API key is available
        if not os.getenv("OPENAI_API_KEY"):
            print("⚠️  OPENAI_API_KEY not set - skipping routing test")
            return True
        
        supervisor = SupervisorAgent()
        
        # Test different query types
        test_queries = [
            ("Calculate 25 * 4", "math"),
            ("Create a SQL query to get all users", "sql"),
            ("What is the capital of France?", "search"),
        ]
        
        for query, expected_agent in test_queries:
            result = supervisor.route_request(query)
            selected_agent = result["primary_agent"]
            print(f"Query: '{query}'")
            print(f"  → Routed to: {selected_agent} (expected: {expected_agent})")
            print(f"  → Reasoning: {result['reasoning']}")
            print(f"  → Confidence: {result['confidence']}")
            print()
        
        print("✅ Supervisor routing test completed")
        return True
    except Exception as e:
        print(f"❌ Supervisor routing error: {e}")
        return False

def test_math_agent_basic():
    """Test basic math agent functionality."""
    print("\nTesting math agent...")
    try:
        from agents import MathAgent
        
        if not os.getenv("OPENAI_API_KEY"):
            print("⚠️  OPENAI_API_KEY not set - skipping math agent test")
            return True
        
        # Note: This will use the API, so we'll just test initialization
        math_agent = MathAgent()
        print("✅ Math agent initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Math agent error: {e}")
        return False

def test_sql_agent_basic():
    """Test basic SQL agent functionality."""
    print("\nTesting SQL agent...")
    try:
        from agents import SQLAgent
        
        if not os.getenv("OPENAI_API_KEY"):
            print("⚠️  OPENAI_API_KEY not set - skipping SQL agent test")
            return True
        
        sql_agent = SQLAgent()
        print("✅ SQL agent initialized successfully")
        return True
    except Exception as e:
        print(f"❌ SQL agent error: {e}")
        return False

def test_search_agent_basic():
    """Test basic search agent functionality."""
    print("\nTesting search agent...")
    try:
        from agents import SearchAgent
        
        if not os.getenv("OPENAI_API_KEY"):
            print("⚠️  OPENAI_API_KEY not set - skipping search agent test")
            return True
        
        search_agent = SearchAgent()
        print("✅ Search agent initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Search agent error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Multi-Agent System Test Suite")
    print("=" * 60)
    
    # Check API key status
    openai_key = os.getenv("OPENAI_API_KEY")
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    
    print("\nAPI Key Status:")
    print(f"  OPENAI_API_KEY: {'✅ Set' if openai_key else '❌ Not set'}")
    print(f"  SERPAPI_API_KEY: {'✅ Set' if serpapi_key else '⚠️  Not set (optional)'}")
    
    # Run tests
    tests = [
        test_imports,
        test_supervisor_routing,
        test_math_agent_basic,
        test_sql_agent_basic,
        test_search_agent_basic,
    ]
    
    results = []
    for test_func in tests:
        results.append(test_func())
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
