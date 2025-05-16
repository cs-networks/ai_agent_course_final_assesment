"""
tavily_search_tool.py
LangChain Tool for searching Tavily and returning results.
"""

from langchain.agents import Tool
from tavily import TavilyClient

import os

import json

def web_search(query: str, limit: int = 3) -> str:
    """
    Search Tavily for a given query string and return up to `limit` results.

    Args:
        query (str): The search term to look up.
        limit (int): Maximum number of search results to return.

    Returns:
        Search results in JSON format.
    """
    try:
        results = TavilyClient(api_key=os.getenv("TAVILY_API_KEY")).search(
            query=query,
            max_results=limit)
        return results
    except Exception as e:
        return f"Error searching Tavily: {str(e)}"


tavily_search_tool = Tool(
    name="web_search",
    func=web_search,
    description="Search The web for a given query string and return up to 3 results."
)

if __name__ == "__main__":
    # Example usage of the tool with a LangChain agent
    from langchain.agents import initialize_agent, AgentType
    from langchain_openai import ChatOpenAI

    import os

    # LLM konfigurieren
    llm = ChatOpenAI(
        model="gpt-4.1-nano-2025-04-14",
        temperature=0.1,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base="https://api.openai.com/v1",
    )
    agent = initialize_agent(
        tools=[tavily_search_tool],
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )


    # Example query
    query = "What is the capital of France and how many people live there?"
    result = agent.invoke(query)
    print(result)
    # Print the result
    # Note: The above code assumes that the agent is set up to handle the query and return a response.