"""SQL Agent for converting natural language to SQL queries."""
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.tools import StructuredTool


class SQLAgent:
    """Agent specialized in generating SQL queries from natural language."""
    
    def __init__(self, llm=None):
        """Initialize the SQL Agent.
        
        Args:
            llm: Language model to use. If None, creates a default ChatOpenAI instance.
        """
        self.llm = llm or ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        self.tools = self._create_tools()
        self.agent = self._create_agent()
    
    def _create_tools(self):
        """Create SQL generation tools."""
        def generate_sql(description: str) -> str:
            """Generate a SQL query from a natural language description.
            
            Args:
                description: Natural language description of the desired query.
                
            Returns:
                A SQL query string.
            """
            prompt = f"""Given the following natural language request, generate a valid SQL query.

Request: {description}

Generate a SQL query that fulfills this request. Include proper SQL syntax with SELECT, FROM, WHERE, JOIN, GROUP BY, ORDER BY, etc. as needed.

Assume standard table and column naming conventions. If the request is ambiguous, make reasonable assumptions and note them in a comment.

SQL Query:"""
            
            try:
                response = self.llm.predict(prompt)
                return response.strip()
            except Exception as e:
                return f"Error generating SQL: {str(e)}"
        
        def validate_sql(query: str) -> str:
            """Validate a SQL query for basic syntax.
            
            Args:
                query: SQL query string to validate.
                
            Returns:
                Validation result.
            """
            # Basic validation checks
            query_upper = query.upper().strip()
            
            if not query_upper:
                return "Error: Empty query"
            
            # Check for basic SQL keywords
            sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER']
            has_keyword = any(keyword in query_upper for keyword in sql_keywords)
            
            if not has_keyword:
                return "Warning: Query does not contain standard SQL keywords"
            
            # Check for balanced parentheses
            if query.count('(') != query.count(')'):
                return "Error: Unbalanced parentheses"
            
            return "Query appears to be valid"
        
        sql_generator = StructuredTool.from_function(
            func=generate_sql,
            name="SQLGenerator",
            description="Generates SQL queries from natural language descriptions. Input should be a clear description of what data you want to query."
        )
        
        sql_validator = StructuredTool.from_function(
            func=validate_sql,
            name="SQLValidator",
            description="Validates SQL query syntax. Input should be a SQL query string."
        )
        
        return [sql_generator, sql_validator]
    
    def _create_agent(self):
        """Create the SQL agent with ReAct prompting."""
        template = """You are a SQL expert. Your job is to help users convert their natural language requests into valid SQL queries.

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
        """Execute a SQL generation query.
        
        Args:
            query: The natural language description of the desired SQL query.
            
        Returns:
            The generated SQL query.
        """
        try:
            result = self.agent.invoke({"input": query})
            return result.get("output", "Could not generate SQL query.")
        except Exception as e:
            return f"Error in SQL Agent: {str(e)}"
