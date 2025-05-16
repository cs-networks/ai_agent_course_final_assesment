"""
arxiv_search_tool.py
LangChain Tool for searching ArXiv and returning results.
"""

from langchain.agents import Tool
from langchain_community.document_loaders import ArxivLoader

def search_arxiv(query: str, limit: int = 5) -> list[dict]:
    """
    Search ArXiv for a given query string and return up to `limit` results.

    Args:
        query (str): The search term to look up.
        limit (int): Maximum number of search results to return.

    Returns:
        list of dict: Each dict contains 'title', 'summary', and 'url'.
    """
    loader = ArxivLoader(query=query, max_results=limit)
    results = loader.load()
    return [{'title': item['title'], 'summary': item['summary'], 'url': item['url']} for item in results]

arxiv_search_tool = Tool(
    name="search_arxiv",
    func=search_arxiv,
    description="Search ArXiv for a given query string and return up to 5 results. Each result contains 'title', 'summary', and 'url'."
)