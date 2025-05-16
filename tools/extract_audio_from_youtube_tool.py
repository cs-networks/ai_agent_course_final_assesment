"""
extrace_audio_from_youtube_tool.py
LangChain Tool for extracting audio from YouTube videos using pytubefix.
This tool allows you to extract audio from YouTube videos and save it in a specified format.
"""

import os

from langchain.agents import Tool
from pytubefix import YouTube
import tempfile

import re
import uuid


def extract_audio_from_youtube(url: str) -> str:
    """
    Extract audio from a YouTube video and save it in the specified format.

    Args:
        url (str): URL of the YouTube video.
        format (str): Format to save the audio (default is "mp3").

    Returns:
        str: Path to the saved audio file.
    """
    try:
        # Create a YouTube object
        youtube_url = re.sub(r'"', '', url)
        yt = YouTube(youtube_url)

        # wähle den besten Audiostream
        stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

        # lade in ein temporäres Verzeichnis
        tmpdir = tempfile.mkdtemp()
        filename = f"downloaded_{uuid.uuid4().hex[:8]}.mp3"
        out_path = stream.download(output_path=tmpdir, filename=filename)



        return f"{out_path}."
    except Exception as e:
        return f"Error extracting audio: {str(e)}"


extract_audio_from_youtube_tool = Tool(
    name="extract_audio_from_youtube",
    func=extract_audio_from_youtube,
    description="Extract audio from a YouTube video and save it in the specified format. Provide the URL of the YouTube video. The audio will be saved in a temporary directory."
)

if __name__ == "__main__":
    # Example usage of the tool with a LangChain agent
    from langchain.agents import initialize_agent, AgentType
    from langchain_openai import ChatOpenAI

    from extract_text_from_audio_tool import extract_text_from_audio_tool

    # LLM konfigurieren
    llm = ChatOpenAI(
        model="gpt-4.1-nano-2025-04-14",
        temperature=0.1,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base="https://api.openai.com/v1",
    )
    agent = initialize_agent(
        tools=[extract_audio_from_youtube_tool, extract_text_from_audio_tool],
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    # Example usage
    query = "Examine the video at https://www.youtube.com/watch?v=1htKBjuUWec.\n\nWhat does Teal'c say in response to the question \"Isn't that hot?\""  # Replace with your YouTube video URL
    result = agent({"input": query})
    print(result)

