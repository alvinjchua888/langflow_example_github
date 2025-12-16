"""Supervisor Agent for routing requests to appropriate specialized agents."""
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from typing import Dict, Any
import json


class SupervisorAgent:
    """Agent that supervises and routes requests to specialized agents."""
    
    def __init__(self, llm=None):
        """Initialize the Supervisor Agent.
        
        Args:
            llm: Language model to use. If None, creates a default ChatOpenAI instance.
        """
        self.llm = llm or ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        self.available_agents = {
            "math": "Handles mathematical computations, calculations, and numerical problems",
            "sql": "Converts natural language to SQL queries and helps with database query generation",
            "search": "Searches Google for current information, facts, news, and general knowledge"
        }
    
    def route_request(self, user_query: str) -> Dict[str, Any]:
        """Analyze the user query and route it to the appropriate agent(s).
        
        Args:
            user_query: The user's input query.
            
        Returns:
            Dictionary containing the selected agent and routing information.
        """
        # Create a prompt for the supervisor to analyze the query
        agents_description = "\n".join([
            f"- {name}: {description}" 
            for name, description in self.available_agents.items()
        ])
        
        prompt = f"""You are a supervisor agent that routes user requests to specialized agents.

Available agents:
{agents_description}

User query: "{user_query}"

Analyze this query and determine which agent(s) should handle it. Consider:
1. What is the primary intent of the query?
2. What type of task is being requested?
3. Which agent is best suited for this task?

Respond in JSON format with the following structure:
{{
    "primary_agent": "agent_name",
    "reasoning": "brief explanation of why this agent was chosen",
    "confidence": "high/medium/low"
}}

Choose only ONE primary agent from: math, sql, search

JSON Response:"""
        
        try:
            response = self.llm.predict(prompt)
            
            # Extract JSON from response
            # Sometimes the model includes markdown code blocks
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            routing_info = json.loads(response.strip())
            
            # Validate the agent choice
            agent_name = routing_info.get("primary_agent", "").lower()
            if agent_name not in self.available_agents:
                # Default to search if uncertain
                agent_name = "search"
                routing_info["primary_agent"] = agent_name
                routing_info["reasoning"] = "Defaulting to search agent due to unclear routing"
            
            return routing_info
            
        except Exception as e:
            # Default routing on error
            return {
                "primary_agent": "search",
                "reasoning": f"Error in routing: {str(e)}. Defaulting to search agent.",
                "confidence": "low"
            }
    
    def get_agent_description(self, agent_name: str) -> str:
        """Get the description of a specific agent.
        
        Args:
            agent_name: Name of the agent.
            
        Returns:
            Agent description.
        """
        return self.available_agents.get(agent_name, "Unknown agent")
    
    def list_agents(self) -> Dict[str, str]:
        """List all available agents and their descriptions.
        
        Returns:
            Dictionary of agent names and descriptions.
        """
        return self.available_agents.copy()
