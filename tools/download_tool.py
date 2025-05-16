"""
download_tool.py
LangChain Tool for downloading files from a given URL.
This tool allows you to download files from the internet and save them locally.
It can be used in various applications, such as downloading datasets, images, or any other files.
"""


import requests
from langchain.agents import Tool

from typing import Optional
import os
from urllib.parse import urlparse
import tempfile


def download_file(url: str, filename: Optional[str] = None) -> str:
    """
    Download a file from a URL and save it to a temporary location.

    Args:
        url: The URL to download from
        filename: Optional filename, will generate one based on URL if not provided

    Returns:
        Path to the downloaded file
    """

    try:
        # Parse URL to get filename if not provided
        if not filename:
            path = urlparse(url).path
            filename = os.path.basename(path)
            if not filename:
                # Generate a random name if we couldn't extract one
                import uuid
                filename = f"downloaded_{uuid.uuid4().hex[:8]}"

        # Create temporary file
        temp_dir = tempfile.gettempdir()
        filepath = os.path.join(temp_dir, filename)

        # Download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Save the file
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return f"File downloaded to {filepath}. You can now process this file."
    except Exception as e:
        return f"Error downloading file: {str(e)}"


download_tool = Tool(
    name="download_file",
    func=download_file,
    description="Lädt eine Datei von einer gegebenen URL herunter und speichert sie lokal."
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
        tools=[download_tool],
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    # Example usage
    url = "https://agents-course-unit4-scoring.hf.space/files/7bd855d8-463d-4ed5-93ca-5fe35145f733"

    # Example query
    query = "Download the file from the given URL and tell me where you stored it on my computer." + f" URL: {url}"
    result = agent.invoke(query)

    print(result)