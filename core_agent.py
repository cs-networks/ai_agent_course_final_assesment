import os

# This is a template for an AI agent that can be used to answer questions and perform tasks.
# It uses the LangChain library to initialize an agent with specific tools and a language model.

import sqlite3
from langchain.agents import initialize_agent, Tool
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from langchain.tools.retriever import create_retriever_tool
from supabase.client import Client, create_client

from langchain_openai import ChatOpenAI

from langchain_core.messages import SystemMessage, HumanMessage

# Tools importieren
from tools.time_tool import time_tool
from tools.download_tool import download_tool
from tools.wiki_search_tool import wiki_page_tool, wiki_search_tool
from tools.math_tools import (
    multiply,
    add,
    subtract,
    divide,
    modulus,
    power_tool,
    logarithm_tool,
    absolute_tool,
    percentage_tool,
    average_tool,
    median_tool,
)
from tools.tavily_search_tool import tavily_search_tool
from tools.arxiv_search_tool import arxiv_search_tool
from tools.defunct_countries_tool import defunct_countries_tool

from tools.extract_text_from_image_tool import extract_text_from_image_tool
from tools.extract_audio_from_youtube_tool import extract_audio_from_youtube_tool
from tools.extract_text_from_audio_tool import extract_text_from_audio_tool

from tools.analyse_excel_file_tool import analyse_excel_tool
from tools.analyse_csv_file_tool import analyse_csv_tool

from tools.python_interpreter_tool import execute_python_code_tool, parse_python_code_tool, execute_python_code_with_output_tool



class AIAgent:
    def __init__(
            self,
            api_key: str = os.getenv("OPENAI_API_KEY"),
            model_name: str = "gpt-4.1-nano-2025-04-14",
            temperature: float = 0.1,
            verbose: bool = True,
            system_prompt_file_name: str = "system_prompt.txt"):
        """
        Initialize the AIAgent with the specified tools and model.

        Args:
            api_key (str): API key for the language model.
            tools (list[Tool]): List of tools to be used by the agent.
            model_name (str): Name of the model to be used.
            temperature (float): Temperature for the model's responses.
            verbose (bool): Whether to print detailed logs.
            system_prompt (str): System prompt to guide the agent's behavior.
        """

        # Set the API key for OpenAI
        if not api_key:
            raise ValueError("API key is required.")

        # System-Prompt laden
        try:
            with open(system_prompt_file_name, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"System prompt file '{system_prompt_file_name}' not found.")
        except Exception as e:
            raise Exception(f"Error reading system prompt file: {e}")

        # System message
        self.sys_msg = SystemMessage(content=self.system_prompt)

        # Embeddings initialisieren
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


        self.supabase: Client = create_client(
            os.environ.get("SUPABASE_URL"),
            os.environ.get("SUPABASE_SERVICE_KEY"))


        self.vector_store = SupabaseVectorStore(
            client=self.supabase,
            embedding= self.embeddings,
            table_name="documents",
            query_name="match_documents_langchain",
        )

        # LLM konfigurieren
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_key=api_key,
            openai_api_base="https://api.openai.com/v1",
        )
        self.verbose = verbose

        # Tools konfigurieren
        self.tools = [  defunct_countries_tool,
                        time_tool, download_tool, wiki_page_tool, wiki_search_tool,
                        tavily_search_tool,
                        arxiv_search_tool,
                        extract_text_from_image_tool,
                        extract_audio_from_youtube_tool,
                        extract_text_from_audio_tool,
                        analyse_excel_tool,
                        analyse_csv_tool,
                        add,
                        subtract,
                        multiply,
                        divide,
                        modulus,
                        power_tool,
                        logarithm_tool,
                        absolute_tool,
                        percentage_tool,
                        average_tool,
                        median_tool,
                        execute_python_code_tool, parse_python_code_tool, execute_python_code_with_output_tool
                      ]

        # Bind tools to the llm
        self.llm_with_tools = self.llm.bind_tools(self.tools)

    # Node
    def assistant(self, state: MessagesState):
        """Assistant node"""
        return {"messages": [self.llm_with_tools.invoke(state["messages"])]}

    #retriever
    def retriever(self, state: MessagesState):
        """Retriever node"""
        # similar_question = vector_store.similarity_search(state["messages"][0].content)
        # example_msg = HumanMessage(
        #     content=f"Here I provide a similar question and answer for reference: \n\n{similar_question[0].page_content}",
        # )
        # return {"messages": [sys_msg] + state["messages"] + [example_msg]}
        similar = self.vector_store.similarity_search(state["messages"][0].content)
        if not similar:
            # Fallback, wenn kein Treffer
            return {"messages": [self.sys_msg] + state["messages"]}
        # ansonsten sicher auf das erste Element zugreifen
        example = HumanMessage(
            content=f"Hier ein ähnliches Beispiel:\n\n{similar[0].page_content}"
        )
        return {"messages": [self.sys_msg] + state["messages"] + [example]}

    def run(self, prompt: str) -> str:
        """Führt den Agent mit dem gegebenen Prompt aus."""
        return self.agent.invoke(prompt)

    def build_graph(self):
        """Baut den Graphen für den Agenten."""
        builder = StateGraph(MessagesState)
        builder.add_node("retriever", self.retriever)
        builder.add_node("assistant", self.assistant)
        builder.add_node("tools", ToolNode(self.tools))
        builder.add_edge(START, "retriever")
        builder.add_edge("retriever", "assistant")
        builder.add_conditional_edges(
            "assistant",
            tools_condition,
        )
        builder.add_edge("tools", "assistant")

        # Compile graph
        return builder.compile()


# Beispiel für die Verwendung des Agenten
if __name__ == "__main__":
    # API-Schlüssel und Modellname angeben
    api_key = os.getenv("OPENAI_API_KEY")
    #model_name = "gpt-4.1-nano-2025-04-14"
    #model_name = "gpt-4.1"
    model_name = "gpt-4o"

    # Agent initialisieren
    agent = AIAgent(api_key=api_key,
                    model_name=model_name,
                    system_prompt_file_name="system_prompt.txt")

    question = "What is the first name of the only Malko Competition recipient from the 20th Century (after 1977) whose nationality on record is a country that no longer exists?"

    # Graph erstellen
    graph = agent.build_graph()


    # Run the graph
    messages = [HumanMessage(content=question)]
    messages = graph.invoke({"messages": messages})
    for m in messages["messages"]:
        m.pretty_print()