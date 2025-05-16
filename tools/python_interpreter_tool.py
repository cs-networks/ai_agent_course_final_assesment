"""
python_interpreter_tool.py
LangChain Tool for executing Python code.
This tool allows you to execute Python code snippets and return the results.
"""

import os

from langchain.agents import Tool
import subprocess
import tempfile
import uuid
import re
import ast
import json
from typing import Any, Dict, List, Optional, Tuple, Union
import sys

import io
import contextlib
import traceback
import pandas as pd
import numpy as np


def execute_python_code(code: str) -> str:
    """
    Execute Python code and return the result.

    Args:
        code (str): Python code to execute.

    Returns:
        str: Result of the execution.
    """
    try:
        # Create a temporary file to store the code
        tmpdir = tempfile.mkdtemp()
        filename = f"code_{uuid.uuid4().hex[:8]}.py"
        filepath = os.path.join(tmpdir, filename)

        # Write the code to the temporary file
        with open(filepath, 'w') as f:
            f.write(code)

        # Execute the code and capture the output
        with io.StringIO() as buf, contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            exec_globals = {}
            exec(code, exec_globals)
            output = buf.getvalue()

        return output
    except Exception as e:
        return f"Error executing code: {str(e)}"
    except SyntaxError as e:
        return f"SyntaxError: {str(e)}"
    except NameError as e:
        return f"NameError: {str(e)}"
    except TypeError as e:
        return f"TypeError: {str(e)}"
    except ValueError as e:
        return f"ValueError: {str(e)}"
    except ZeroDivisionError as e:
        return f"ZeroDivisionError: {str(e)}"

def parse_python_code(code: str) -> str:
    """
    Parse Python code and return the abstract syntax tree (AST) representation.

    Args:
        code (str): Python code to parse.

    Returns:
        str: AST representation of the code.
    """
    try:
        # Parse the code into an AST
        tree = ast.parse(code)
        return ast.dump(tree, indent=4)
    except Exception as e:
        return f"Error parsing code: {str(e)}"

def execute_python_code_with_output(code: str) -> str:
    """
    Execute Python code and return the result.

    Args:
        code (str): Python code to execute.

    Returns:
        str: Result of the execution.
    """
    try:
        # Create a temporary file to store the code
        tmpdir = tempfile.mkdtemp()
        filename = f"code_{uuid.uuid4().hex[:8]}.py"
        filepath = os.path.join(tmpdir, filename)

        # Write the code to the temporary file
        with open(filepath, 'w') as f:
            f.write(code)

        # Execute the code and capture the output
        with io.StringIO() as buf, contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            exec_globals = {}
            exec(code, exec_globals)
            output = buf.getvalue()

        return output
    except Exception as e:
        return f"Error executing code: {str(e)}"
    except SyntaxError as e:
        return f"SyntaxError: {str(e)}"



execute_python_code_tool = Tool(
    name="execute_python_code",
    func=execute_python_code,
    description="Execute Python code and return the result. Provide the Python code as a string."
)

parse_python_code_tool = Tool(
    name="parse_python_code",
    func=parse_python_code,
    description="Parse Python code and return the abstract syntax tree (AST) representation. Provide the Python code as a string."
)

execute_python_code_with_output_tool = Tool(
    name="execute_python_code_with_output",
    func=execute_python_code_with_output,
    description="Execute Python code and return the result. Provide the Python code as a string."
)

if __name__ == "__main__":
    # Example usage of the tool with a LangChain agent
    from langchain.agents import initialize_agent, AgentType
    from langchain_openai import ChatOpenAI

    # LLM konfigurieren
    llm = ChatOpenAI(
        model="gpt-4.1-nano-2025-04-14",
        temperature=0.1,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base="https://api.openai.com/v1",
    )
    agent = initialize_agent(
        tools=[execute_python_code_tool],
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    # Example usage
    code = """
    #print("Hello, World!")
    x = 5
    y = 10
    result = x + y
    print("The result is:", result)
    """
    result = agent.run(code)
    print(result)
