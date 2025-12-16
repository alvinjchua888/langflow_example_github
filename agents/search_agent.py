"""Search Agent for finding information from Google."""
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.tools import StructuredTool
from langchain_community.utilities import SerpAPIWrapper
import os


class SearchAgent:
    """Agent specialized in searching for information using Google."""
    
    def __init__(self, llm=None):
        """Initialize the Search Agent.
        
        Args:
            llm: Language model to use. If None, creates a default ChatOpenAI instance.
        """
        self.llm = llm or ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        self.tools = self._create_tools()
        self.agent = self._create_agent()
    
    def _create_tools(self):
        """Create search tools."""
        def search_google(query: str) -> str:
            """Search Google for information.
            
            Args:
                query: The search query.
                
            Returns:
                Search results.
            """
            try:
                # Check if SERPAPI key is available
                serpapi_key = os.getenv("SERPAPI_API_KEY")
                if not serpapi_key:
                    return "Error: SERPAPI_API_KEY not found. Please set it in your .env file to use the search functionality."
                
                search = SerpAPIWrapper()
                result = search.run(query)
                return result
            except Exception as e:
                return f"Error performing search: {str(e)}"
        
        def summarize_results(text: str) -> str:
            """Summarize search results into key points.
            
            Args:
                text: Text to summarize.
                
            Returns:
                Summarized text.
            """
            try:
                prompt = f"""Summarize the following information into clear, concise key points:

{text}

Summary:"""
                response = self.llm.predict(prompt)
                return response.strip()
            except Exception as e:
                return f"Error summarizing: {str(e)}"
        
        google_search = StructuredTool.from_function(
            func=search_google,
            name="GoogleSearch",
            description="Useful for searching the internet for current information, facts, news, and general knowledge. Input should be a search query string."
        )
        
        summarizer = StructuredTool.from_function(
            func=summarize_results,
            name="Summarizer",
            description="Useful for summarizing long text into key points. Input should be the text to summarize."
        )
        
        return [google_search, summarizer]
    
    def _create_agent(self):
        """Create the search agent with ReAct prompting."""
        template = """You are a research assistant expert at finding information on the internet. Your job is to help users find accurate and relevant information using Google search.

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

        prompt = PromptTemplate.from_template(template)
        agent = create_react_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True, handle_parsing_errors=True)
    
    def run(self, query: str) -> str:
        """Execute a search query.
        
        Args:
            query: The search question or query.
            
        Returns:
            Search results and answer.
        """
        try:
            result = self.agent.invoke({"input": query})
            return result.get("output", "Could not find information.")
        except Exception as e:
            return f"Error in Search Agent: {str(e)}"
