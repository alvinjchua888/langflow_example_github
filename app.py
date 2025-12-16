"""Main Streamlit application for the Multi-Agent System."""
import streamlit as st
import os
from dotenv import load_dotenv
from agents import MathAgent, SQLAgent, SearchAgent, SupervisorAgent
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Chat System",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agents_initialized" not in st.session_state:
    st.session_state.agents_initialized = False


@st.cache_resource
def initialize_agents():
    """Initialize all agents with shared LLM."""
    try:
        # Check for OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("⚠️ OPENAI_API_KEY not found. Please set it in your .env file.")
            return None
        
        # Create shared LLM instance
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        
        # Initialize all agents
        agents = {
            "supervisor": SupervisorAgent(llm),
            "math": MathAgent(llm),
            "sql": SQLAgent(llm),
            "search": SearchAgent(llm)
        }
        
        return agents
    except Exception as e:
        st.error(f"Error initializing agents: {str(e)}")
        return None


def get_agent_emoji(agent_name: str) -> str:
    """Get emoji for each agent type."""
    emojis = {
        "supervisor": "🎯",
        "math": "🔢",
        "sql": "💾",
        "search": "🔍"
    }
    return emojis.get(agent_name, "🤖")


def process_user_query(query: str, agents: dict) -> dict:
    """Process user query through the multi-agent system.
    
    Args:
        query: User's input query.
        agents: Dictionary of initialized agents.
        
    Returns:
        Dictionary containing the response and metadata.
    """
    # Step 1: Supervisor routes the request
    supervisor = agents["supervisor"]
    routing_info = supervisor.route_request(query)
    
    selected_agent = routing_info["primary_agent"]
    reasoning = routing_info["reasoning"]
    
    # Step 2: Execute with the selected agent
    agent = agents.get(selected_agent)
    if agent:
        response = agent.run(query)
    else:
        response = "Error: Selected agent not available."
    
    return {
        "response": response,
        "agent": selected_agent,
        "reasoning": reasoning,
        "confidence": routing_info.get("confidence", "unknown")
    }


def main():
    """Main application function."""
    # Title and description
    st.title("🤖 Multi-Agent Chat System")
    st.markdown("""
    This is an intelligent multi-agent system powered by LangChain and OpenAI. 
    The supervisor agent automatically routes your queries to the most appropriate specialized agent:
    
    - 🔢 **Math Agent**: Handles calculations and mathematical problems
    - 💾 **SQL Agent**: Converts natural language to SQL queries
    - 🔍 **Search Agent**: Finds information from Google
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # API Key status
        st.subheader("API Keys")
        openai_key_set = bool(os.getenv("OPENAI_API_KEY"))
        serpapi_key_set = bool(os.getenv("SERPAPI_API_KEY"))
        
        st.write("OpenAI API Key:", "✅" if openai_key_set else "❌")
        st.write("SerpAPI Key:", "✅" if serpapi_key_set else "❌")
        
        if not openai_key_set:
            st.warning("Please set OPENAI_API_KEY in .env file")
        if not serpapi_key_set:
            st.info("Set SERPAPI_API_KEY in .env file to enable Google Search")
        
        st.divider()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        st.divider()
        
        st.subheader("📚 Example Queries")
        st.markdown("""
        **Math:**
        - Calculate 15% of 250
        - What is the square root of 144?
        
        **SQL:**
        - Get all users who registered after 2023
        - Query to find top 10 products by sales
        
        **Search:**
        - What is the weather in Paris today?
        - Latest news about AI developments
        """)
    
    # Initialize agents
    agents = initialize_agents()
    
    if agents is None:
        st.error("Failed to initialize agents. Please check your API keys and try again.")
        return
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display agent info for assistant messages
            if message["role"] == "assistant" and "agent" in message:
                with st.expander("🔍 Agent Details"):
                    st.write(f"**Agent Used:** {get_agent_emoji(message['agent'])} {message['agent'].upper()}")
                    st.write(f"**Reasoning:** {message.get('reasoning', 'N/A')}")
                    st.write(f"**Confidence:** {message.get('confidence', 'N/A')}")
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process query and get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = process_user_query(prompt, agents)
                
                response = result["response"]
                agent_used = result["agent"]
                reasoning = result["reasoning"]
                confidence = result["confidence"]
                
                st.markdown(response)
                
                # Show agent details
                with st.expander("🔍 Agent Details"):
                    st.write(f"**Agent Used:** {get_agent_emoji(agent_used)} {agent_used.upper()}")
                    st.write(f"**Reasoning:** {reasoning}")
                    st.write(f"**Confidence:** {confidence}")
        
        # Add assistant message to chat
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "agent": agent_used,
            "reasoning": reasoning,
            "confidence": confidence
        })


if __name__ == "__main__":
    main()
