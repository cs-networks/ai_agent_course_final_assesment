"""
extract_text_from_audio.py
LangChain Tool for extracting text from audio files using Whisper.
This tool allows you to extract text from audio files using Whisper.
"""


import os
from langchain.agents import Tool
import whisper


def extract_text_from_audio(audio_path: str) -> str:
    """
    Extract text from an audio file using Whisper.

    Args:
        audio_path (str): Path to the audio file.

    Returns:
        str: Extracted text from the audio.
    """
    try:
        # Load the Whisper model
        model = whisper.load_model("base")

        # Transcribe the audio file
        result = model.transcribe(audio_path)
        return "Extracted text: " + result["text"] + "\n" + "[END OF TEXT]"
    except FileNotFoundError:
        return f"Error: The file {audio_path} was not found."
    except Exception as e:
        return f"Error extracting text from audio: {str(e)}"

extract_text_from_audio_tool = Tool(
    name="extract_text_from_audio",
    func=extract_text_from_audio,
    description="Extract text from an audio file using Whisper. Provide the path to the audio file. The Text will be returned in a string format and ended with [END OF TEXT]."
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
        tools=[extract_text_from_audio_tool],
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    # Example usage
    audio_path = "./testfiles/sample.mp3"  # Replace with your audio path
    query = "Hi, I'm making a pie but I could use some help with my shopping list. I have everything I need for the crust, but I'm not sure about the filling. I got the recipe from my friend Aditi, but she left it as a voice memo and the speaker on my phone is buzzing so I can't quite make out what she's saying. Could you please listen to the recipe and list all of the ingredients that my friend described? I only want the ingredients for the filling, as I have everything I need to make my favorite pie crust. I've attached the recipe as Strawberry pie.mp3.\n\nIn your response, please only list the ingredients, not any measurements. So if the recipe calls for \"a pinch of salt\" or \"two cups of ripe strawberries\" the ingredients on the list would be \"salt\" and \"ripe strawberries\".\n\nPlease format your response as a comma separated list of ingredients. Also, please alphabetize the ingredients. \n\nThanks so much for your help! I really appreciate it.\n\nFile:" + audio_path
    result = agent({"input": query})
    print(result)

