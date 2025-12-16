"""Math Agent for handling mathematical computations."""
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.tools import StructuredTool
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
        self.tools = self._create_tools()
        self.agent = self._create_agent()
    
    def _create_tools(self):
        """Create mathematical computation tools."""
        def calculate(expression: str) -> str:
            """Evaluate a mathematical expression safely.
            
            Args:
                expression: A mathematical expression as a string.
                
            Returns:
                The result of the calculation.
            """
            try:
                # Remove any non-mathematical characters for safety
                safe_expr = re.sub(r'[^0-9+\-*/().\s]', '', expression)
                
                # Create a safe evaluation environment with math functions
                safe_dict = {
                    '__builtins__': {},
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
                
                result = eval(safe_expr, safe_dict)
                return f"The result is: {result}"
            except Exception as e:
                return f"Error calculating expression: {str(e)}"
        
        calculator = StructuredTool.from_function(
            func=calculate,
            name="Calculator",
            description="Useful for performing mathematical calculations. Input should be a valid mathematical expression."
        )
        
        return [calculator]
    
    def _create_agent(self):
        """Create the math agent with ReAct prompting."""
        template = """You are a mathematical computation expert. Your job is to help solve mathematical problems and perform calculations.

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
        """Execute a mathematical query.
        
        Args:
            query: The mathematical question or expression.
            
        Returns:
            The result of the computation.
        """
        try:
            result = self.agent.invoke({"input": query})
            return result.get("output", "Could not compute the result.")
        except Exception as e:
            return f"Error in Math Agent: {str(e)}"
