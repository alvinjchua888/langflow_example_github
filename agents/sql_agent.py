"""SQL Agent for converting natural language to SQL queries."""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


class SQLAgent:
    """Agent specialized in generating SQL queries from natural language."""
    
    def __init__(self, llm=None):
        """Initialize the SQL Agent.
        
        Args:
            llm: Language model to use. If None, creates a default ChatOpenAI instance.
        """
        self.llm = llm or ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    
    def _validate_sql(self, query: str) -> str:
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
        
        return "Valid"
    
    def run(self, query: str) -> str:
        """Execute a SQL generation query.
        
        Args:
            query: The natural language description of the desired SQL query.
            
        Returns:
            The generated SQL query.
        """
        try:
            # Create a prompt for the LLM to generate SQL
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a SQL expert. Your job is to convert natural language requests into valid SQL queries.

Guidelines:
1. Generate syntactically correct SQL queries
2. Use proper SQL syntax with SELECT, FROM, WHERE, JOIN, GROUP BY, ORDER BY, etc. as needed
3. Assume standard table and column naming conventions (lowercase with underscores)
4. If the request is ambiguous, make reasonable assumptions
5. Include comments for clarification if needed
6. Return only the SQL query, properly formatted

Example table structures you can assume:
- users (id, name, email, created_at, updated_at)
- products (id, name, price, category, stock, created_at)
- orders (id, user_id, product_id, quantity, order_date, status)
- customers (id, name, email, phone, address, registration_date)
"""),
                ("user", "{query}")
            ])
            
            # Get the SQL from the LLM
            chain = prompt | self.llm
            response = chain.invoke({"query": query})
            sql_query = response.content.strip()
            
            # Remove markdown code blocks if present
            if "```sql" in sql_query:
                sql_query = sql_query.split("```sql")[1].split("```")[0].strip()
            elif "```" in sql_query:
                sql_query = sql_query.split("```")[1].split("```")[0].strip()
            
            # Validate the query
            validation_result = self._validate_sql(sql_query)
            
            if validation_result == "Valid":
                return f"Generated SQL Query:\n\n```sql\n{sql_query}\n```"
            else:
                return f"Generated SQL Query (with warning):\n\n```sql\n{sql_query}\n```\n\nValidation: {validation_result}"
                
        except Exception as e:
            return f"Error in SQL Agent: {str(e)}"
