"""
analyse_csv_file_tool.py
LangChain Tool for analyzing CSV files.
This tool allows you to analyze CSV files and extract useful information from them.
"""

import pandas as pd
from langchain.agents import Tool
import os
from typing import Optional

def analyse_csv_file(file_path: str, column_name: Optional[str] = None) -> str:
    """
    Analyze a CSV file and return basic statistics or information about a specific column.

    Args:
        file_path (str): Path to the CSV file.
        column_name (str, optional): Name of the column to analyze. If None, returns general info.

    Returns:
        str: Analysis result.
    """
    try:
        # Check if the file exists
        if not os.path.isfile(file_path):
            return f"Error: The file {file_path} does not exist."

        # Read the CSV file
        df = pd.read_csv(file_path)

        # If no column name is provided, return general info
        if column_name is None:
            return df.describe().to_string()

        # Check if the column exists
        if column_name not in df.columns:
            return f"Error: The column '{column_name}' does not exist in the CSV file."

        # Return statistics for the specified column
        return df[column_name].describe().to_string()

    except Exception as e:
        return f"Error analyzing CSV file: {str(e)}"

analyse_csv_tool = Tool(
    name="analyse_csv_file",
    func=analyse_csv_file,
    description="Analyze a CSV file and return basic statistics or information about a specific column. Provide the path to the CSV file and optionally the column name."
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
        tools=[analyse_csv_tool],
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    # Example usage
    file_path = "./testfiles/sample.csv"  # Replace with your CSV file path
    result = agent.invoke(f"Analyse the CSV file at {file_path} and provide statistics.")
    print(result)