"""Search Agent for finding information from Google."""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
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
    
    def _search_google(self, query: str) -> str:
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
                return None
            
            search = SerpAPIWrapper()
            result = search.run(query)
            return result
        except Exception as e:
            return None
    
    def run(self, query: str) -> str:
        """Execute a search query.
        
        Args:
            query: The search question or query.
            
        Returns:
            Search results and answer.
        """
        try:
            # Try to search using SerpAPI if available
            search_results = self._search_google(query)
            
            if search_results:
                # Summarize the search results
                prompt = ChatPromptTemplate.from_messages([
                    ("system", """You are a research assistant. Analyze the search results and provide a clear, 
concise answer to the user's question. Include relevant facts and cite the information appropriately.
Format your response in a user-friendly way with key points."""),
                    ("user", f"Question: {query}\n\nSearch Results:\n{search_results}")
                ])
                
                chain = prompt | self.llm
                response = chain.invoke({})
                return response.content
            else:
                # If SerpAPI is not available, use the LLM's knowledge
                prompt = ChatPromptTemplate.from_messages([
                    ("system", """You are a knowledgeable research assistant. Answer the user's question 
based on your training data. Be accurate and informative. If you're not certain about something, 
say so. Note that your knowledge may not include very recent events."""),
                    ("user", "{query}")
                ])
                
                chain = prompt | self.llm
                response = chain.invoke({"query": query})
                
                # Add a note about SerpAPI
                note = "\n\n*Note: SERPAPI_API_KEY not configured. This answer is based on my training data, not live search. For real-time information, please set up SerpAPI.*"
                return response.content + note
                
        except Exception as e:
            return f"Error in Search Agent: {str(e)}"
