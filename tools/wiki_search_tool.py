"""
wikipedia_tool.py
LangChain Tool for fetching full Wikipedia page content.
"""

from langchain.agents import Tool

import requests


def search_wikipedia(query: str, limit: int = 5) -> list[dict]:
    """
    Search Wikipedia for a given query string and return up to `limit` results.

    Args:
        query (str): The search term to look up.
        limit (int): Maximum number of search results to return.

    Returns:
        list of dict: Each dict contains 'title' and 'snippet'.
    """
    endpoint = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': query,
        'srlimit': limit,
        'format': 'json',
        'srprop': 'snippet'
    }
    resp = requests.get(endpoint, params=params)
    resp.raise_for_status()
    data = resp.json().get('query', {}).get('search', [])
    return [{'title': item['title'], 'snippet': item['snippet']} for item in data]

def get_wikipedia_page(title: str) -> str:
    """
    Retrieve the full HTML content of a Wikipedia page by title.

    Args:
        title (str): The exact title of the Wikipedia page.

    Returns:
        str: HTML content of the page.
    """
    endpoint = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'parse',
        'page': title,
        'format': 'json',
        'prop': 'text'
    }
    resp = requests.get(endpoint, params=params)
    resp.raise_for_status()
    return resp.json().get('parse', {}).get('text', {}).get('*', '')

wiki_search_tool = Tool(
    name="search_wikipedia",
    func=search_wikipedia,
    description="Search Wikipedia for a given query string and return up to 5 results. Each result contains 'title' and 'snippet'."
)

wiki_page_tool = Tool(
    name="get_wikipedia_page",
    func=get_wikipedia_page,
    description="Retrieve the full HTML content of a Wikipedia page by title. Provide the exact title of the Wikipedia page."
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
        tools=[wiki_search_tool, wiki_page_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION ,
        verbose=True,
    )

    # Run the agent with a sample query
    result = agent.run("Tell my about python programming language.")
    print(result)



