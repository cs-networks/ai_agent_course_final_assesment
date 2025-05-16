"""
defunct_countries_tool.py
LangChain Tool for fetching defunct countries and their dates.
"""

from langchain.agents import Tool
import json

def get_defunct_countries(_: str = "") -> str:
    """Returns a JSON-formatted list of countries that no longer exist.

    Args:
        _: Optional string argument (not used)
    Returns:
        JSON-formatted string containing country names, dissolution dates, and successors.
    """
    data = [
        {"name": "Czechoslovakia", "dissolution_date": "1992-12-31", "successors": ["Czech Republic", "Slovakia"]},
        {"name": "Socialist Federal Republic of Yugoslavia", "dissolution_date": "1992-04-27", "successors": [
            "Bosnia and Herzegovina", "Croatia", "North Macedonia", "Slovenia", "Federal Republic of Yugoslavia"
        ]},
        {"name": "Soviet Union", "dissolution_date": "1991-12-26", "successors": [
            "Russia", "Ukraine", "Belarus", "Estonia", "Latvia", "Lithuania", "Moldova",
            "Armenia", "Azerbaijan", "Georgia", "Kazakhstan", "Kyrgyzstan", "Tajikistan",
            "Turkmenistan", "Uzbekistan"
        ]},
        {"name": "East Germany", "dissolution_date": "1990-10-03", "successors": ["Germany"]},
        {"name": "West Germany", "dissolution_date": "1990-10-03", "successors": ["Germany"]},
        {"name": "Yemen Arab Republic (North Yemen)", "dissolution_date": "1990-05-22", "successors": ["Republic of Yemen"]},
        {"name": "People's Democratic Republic of Yemen (South Yemen)", "dissolution_date": "1990-05-22", "successors": ["Republic of Yemen"]},
        {"name": "Republic of Vietnam (South Vietnam)", "dissolution_date": "1975-05-30", "successors": ["Socialist Republic of Vietnam"]},
        {"name": "United Republic of Tanganyika and Zanzibar (Tanzania precursor)", "dissolution_date": "1964-04-26", "successors": ["Tanzania"]},
        {"name": "Tanganyika", "dissolution_date": "1964-04-26", "successors": ["Tanzania"]},
        {"name": "Sultanate of Zanzibar", "dissolution_date": "1964-04-26", "successors": ["Tanzania"]},
        {"name": "Federation of Rhodesia and Nyasaland", "dissolution_date": "1963-12-31", "successors": [
            "Malawi", "Zambia", "Rhodesia (now Zimbabwe)"
        ]},
        {"name": "United Arab Republic", "dissolution_date": "1961-09-28", "successors": ["Egypt"]},
        {"name": "Mali Federation", "dissolution_date": "1960-08-20", "successors": ["Senegal", "Mali"]}
    ]
    return json.dumps(data, indent=2)

defunct_countries_tool = Tool(
    name="get_defunct_countries",
    func=get_defunct_countries,
    description="Returns a JSON-formatted list of countries that no longer exist, including their dissolution dates and successors."
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
        tools=[defunct_countries_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION ,
        verbose=True,
    )

    # Run the agent with a sample query
    result = agent.run("When did Czechoslovakia dissolve and what were its successors?")
    print(result)
