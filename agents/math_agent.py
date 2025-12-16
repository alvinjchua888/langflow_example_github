"""Math Agent for handling mathematical computations."""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import re
import math


class MathAgent:
    """Agent specialized in mathematical computations."""
    
    def __init__(self, llm=None):
        """Initialize the Math Agent.
        
        Args:
            llm: Language model to use. If None, creates a default ChatOpenAI instance.
        """
        self.llm = llm or ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    
    def _calculate(self, expression: str) -> str:
        """Evaluate a mathematical expression safely.
        
        Args:
            expression: A mathematical expression as a string.
            
        Returns:
            The result of the calculation.
        """
        try:
            # Remove any potentially harmful characters, keep only math-related ones
            # Allow digits, operators, parentheses, spaces, and function names
            allowed_pattern = r'[^0-9+\-*/().sqrt()sincotanlgexpi\s]'
            safe_expr = re.sub(allowed_pattern, '', expression)
            
            # Create a restricted evaluation environment with math functions
            # Using __builtins__: {} prevents access to built-in functions like exec, eval, open, etc.
            safe_dict = {
                '__builtins__': {},  # No built-in functions
                'abs': abs,
                'round': round,
                'min': min,
                'max': max,
                'sum': sum,
                'pow': pow,
                'sqrt': math.sqrt,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'log': math.log,
                'exp': math.exp,
                'pi': math.pi,
                'e': math.e,
            }
            
            # Evaluate with restricted namespace and builtins disabled
            # This is still eval() but heavily restricted to only mathematical operations
            result = eval(safe_expr, {"__builtins__": {}}, safe_dict)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def run(self, query: str) -> str:
        """Execute a mathematical query.
        
        Args:
            query: The mathematical question or expression.
            
        Returns:
            The result of the computation.
        """
        try:
            # Create a prompt for the LLM to extract the mathematical expression
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a mathematical computation expert. 
Your job is to:
1. Extract the mathematical expression from the user's query
2. Simplify it to a calculable expression using basic operators (+, -, *, /, parentheses)
3. Return only the expression to calculate

If the query asks for special functions like sqrt, sin, cos, use the Python format: sqrt(x), sin(x), etc.
Include 'pi' or 'e' if needed."""),
                ("user", "{query}")
            ])
            
            # Get the expression from the LLM
            chain = prompt | self.llm
            response = chain.invoke({"query": query})
            expression = response.content.strip()
            
            # Calculate the result
            result = self._calculate(expression)
            
            # If calculation succeeded, return a formatted answer
            if not result.startswith("Error"):
                return f"The answer is: {result}"
            else:
                # If calculation failed, let the LLM explain the problem
                explanation_prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a mathematical expert. Solve the following problem and explain your answer clearly."),
                    ("user", "{query}")
                ])
                chain = explanation_prompt | self.llm
                response = chain.invoke({"query": query})
                return response.content
                
        except Exception as e:
            return f"Error in Math Agent: {str(e)}"
