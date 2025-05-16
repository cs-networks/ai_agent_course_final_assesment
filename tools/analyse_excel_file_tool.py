"""
analyse_csv_file_tool.py
LangChain Tool for analyzing Excel files.
This tool allows you to analyze Excel files and extract useful information from them.
"""

import pandas as pd
from langchain.agents import Tool
import os
from typing import Optional


def analyse_excel_file(file_path: str, sheet_name: Optional[str] = None) -> str:
    """
    Analyze an Excel file and return basic statistics or information about a specific sheet.

    Args:
        file_path (str): Path to the Excel file.
        sheet_name (str, optional): Name of the sheet to analyze. If None, returns general info.

    Returns:
        str: Analysis result.
    """
    try:
        # Check if the file exists
        if not os.path.isfile(file_path):
            return f"Error: The file {file_path} does not exist."

        # Read the Excel file
        if sheet_name is None:
            df = pd.read_excel(file_path)
        else:
            df = pd.read_excel(file_path, sheet_name=sheet_name)

        # Run various analyses based on the query
        result = f"Excel file loaded with {len(df)} rows and {len(df.columns)} columns.\n"
        result += f"Columns: {', '.join(df.columns)}\n\n"

        # Add summary statistics
        result += "Summary statistics:\n"
        result += str(df.describe())

        # If no sheet name is provided, return general info
        return result

    except Exception as e:
        return f"Error analyzing Excel file: {str(e)}"

analyse_excel_tool = Tool(
    name="analyse_excel_file",
    func=analyse_excel_file,
    description="Analyze an Excel file and return basic statistics or information about a specific sheet. Provide the path to the Excel file and optionally the sheet name."
)

if __name__ == "__main__":
    # Example usage of the tool with a LangChain agent
    from langchain.agents import initialize_agent, AgentType
    from langchain_openai import ChatOpenAI

    from math_tools import add_tool, subtract_tool, multiply_tool, divide_tool

    # LLM konfigurieren
    llm = ChatOpenAI(
        model="gpt-4.1-nano-2025-04-14",
        temperature=0.1,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base="https://api.openai.com/v1",
    )
    agent = initialize_agent(
        tools=[analyse_excel_tool],
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    # Example usage
    file_path = "./testfiles/sample.xlsx"  # Replace with your Excel file path
    query = "The attached Excel file contains the sales of menu items for a local fast-food chain. What were the total sales that the chain made from food (not including drinks)? Express your answer in USD with two decimal places." + "File path: " + file_path + " "

    result = agent.invoke({"input": query})
    print(result)
