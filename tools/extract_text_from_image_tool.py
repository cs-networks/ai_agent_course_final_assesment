"""
extract_text_from_image_tool.py

LangChain Tool for extracting text from images using Tesseract OCR.
This tool allows you to extract text from images using Tesseract OCR.
It can be used in various applications, such as document processing, image analysis, and more.
"""


from langchain.agents import Tool
import pytesseract
from PIL import Image

import os

def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image using Tesseract OCR.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Extracted text from the image.
    """
    try:
        # Open the image file
        with Image.open(image_path) as img:
            # Use Tesseract to do OCR on the image
            text = pytesseract.image_to_string(img)
        return "Extracted text: " + text + "\n" + "[END OF TEXT]"
    except FileNotFoundError:
        return f"Error: The file {image_path} was not found."
    except pytesseract.TesseractError:
        return "Error: Tesseract OCR failed to process the image. Please ensure Tesseract is installed and configured correctly."
    except Exception as e:
        return f"Error extracting text from image: {str(e)}"

extract_text_from_image_tool = Tool(
    name="extract_text_from_image",
    func=extract_text_from_image,
    description="Extract text from an image using Tesseract OCR. Provide the path to the image file. The Text will be returned in a string format and ended with [END OF TEXT]."
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
        tools=[extract_text_from_image_tool],
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    # Example usage
    image_path = "./testfiles/image.jpg"  # Replace with your image path
    query = f"Extract an multiline text from the image at {image_path} and telkl me what it is about."
    response = agent.invoke({"input": query})

    print(response)
