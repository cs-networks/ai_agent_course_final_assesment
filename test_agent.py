#!/usr/bin/env python3
"""
Test script for the GAIA agent using real API keys.
This script simulates GAIA benchmark questions and helps debug/improve the agent.
"""

import os
from core_agent import AIAgent
from langchain_core.messages import HumanMessage

SAMPLE_QUESTIONS = [
    # {
    #     "task_id": "task_001",
    #     "question": "What is the capital of France?",
    #     "expected_answer": "Paris",
    #     "has_file": False,
    #     "file_content": None
    # },
#     {
#         "task_id": "task_002",
#         "question": "What is the square root of 144?",
#         "expected_answer": "12",
#         "has_file": False,
#         "file_content": None
#     },
#     {
#         "task_id": "task_003",
#         "question": "If a train travels at 60 miles per hour, how far will it travel in 2.5 hours?",
#         "expected_answer": "150 miles",
#         "has_file": False,
#         "file_content": None
#     },
#     {
#         "task_id": "task_004",
#         "question": ".rewsna eht sa 'thgir' drow eht etirw ,tfel fo etisoppo eht si tahW",
#         "expected_answer": "right",
#         "has_file": False,
#         "file_content": None
#     },
#     {
#         "task_id": "task_005",
#         "question": "Analyze the data in the attached CSV file and tell me the total sales for the month of January.",
#         "expected_answer": "$10,250.75",
#         "has_file": True,
#         "file_content": """Date,Product,Quantity,Price,Total
# 2023-01-05,Widget A,10,25.99,259.90
# 2023-01-12,Widget B,5,45.50,227.50
# 2023-01-15,Widget C,20,50.25,1005.00
# 2023-01-20,Widget A,15,25.99,389.85
# 2023-01-25,Widget B,8,45.50,364.00
# 2023-01-28,Widget D,100,80.04,8004.50"""
#     },
#     {
#         "task_id": "task_006",
#         "question": "I'm making a grocery list for my mom, but she's a picky eater. She only eats foods that don't contain the letter 'e'. List 5 common fruits and vegetables she can eat.",
#         "expected_answer": "Banana, Kiwi, Corn, Fig, Taro",
#         "has_file": False,
#         "file_content": None
#     },
#     {
#         "task_id": "task_007",
#         "question": "How many studio albums were published by Mercedes Sosa between 1972 and 1985?",
#         "expected_answer": "12",
#         "has_file": False,
#         "file_content": None
#     },
#     {
#         "task_id": "task_008",
#         "question": "In the video https://www.youtube.com/watch?v=L1vXC1KMRd0, what color is primarily associated with the main character?",
#         "expected_answer": "Blue",
#         "has_file": False,
#         "file_content": None
#     },
#     {
#         "task_id": "task_009",
#         "question": "What is the capital of Germany?",
#         "expected_answer": "Berlin",
#         "has_file": False,
#         "file_content": None
#     },
#     {
#         "task_id": "task_010",
#         "question": "What is the chemical symbol for gold?",
#         "expected_answer": "Au",
#         "has_file": False,
#         "file_content": None
#     },
#     {
#         "task_id": "task_011",
#         "question": "What is the largest planet in our solar system?",
#         "expected_answer": "Jupiter",
#         "has_file": False,
#         "file_content": None
#     },
    {
        "task_id": "task_012",
        "question": "What's the time in London if it's 3 PM in New York?",
        "expected_answer": "8 PM",
        "has_file": False,
        "file_content": None
    },
    {
        "task_id": "task_013",
        "question": "What's the time in New York right now?",
        "expected_answer": "04:12",
        "has_file": False,
        "file_content": None
    },
]


# Beispiel für die Verwendung des Agenten
if __name__ == "__main__":
    # API-Schlüssel und Modellname angeben
    api_key = os.getenv("OPENAI_API_KEY")
    #model_name = "gpt-4.1-nano-2025-04-14"
    model_name = "gpt-4.1"

    # Agent initialisieren
    agent = AIAgent(api_key=api_key,
                    model_name=model_name,
                    system_prompt_file_name="system_prompt.txt")

    # Fragen durchlaufen und Agenten ausführen

    # Graph erstellen
    graph = agent.build_graph()


    # Run the graph

    total_count = len(SAMPLE_QUESTIONS)

    for idx, question_data in enumerate(SAMPLE_QUESTIONS):
        task_id = question_data["task_id"]
        question = question_data["question"]
        expected = question_data["expected_answer"]

        print(f"\n{'='*80}")
        print(f"Question {idx+1}/{total_count}: {question}")
        print(f"Expected: {expected}")

        # Wrap the question in a HumanMessage from langchain_core
        messages = [HumanMessage(content=question)]
        messages = graph.invoke({"messages": messages})
        answer = messages['messages'][-1].content

        # Find the index of "FINAL ANSWER:" and slice from there
        idx = answer.find("FINAL ANSWER:")
        if idx != -1:
            result = answer[idx:].strip()
            # Remove any leading or trailing whitespace
            result = result.strip()
        # If "FINAL ANSWER:" is not found, use the entire answer
        # (this is a fallback, but ideally we should always have "FINAL ANSWER:")
        else:
            result = answer

        print(f"Answer: {result}")

        # Check if the answer matches the expected answer
        if answer[14:] == expected:
            print(f"Task {task_id} passed.")
        else:
            print(f"Task {task_id} failed. Expected: {expected}, Got: {answer[14:]}")
        print(f"{'='*80}")
        # Optional: Add a delay between questions to avoid hitting API rate limits
        # time.sleep(1)
        # Optional: Save the results to a file or database for further analysis
        with open("results.txt", "a") as f:
            f.write(f"Task {task_id}: {answer[14:]}\n")
        # Optional: Add a delay between questions to avoid hitting API rate limits
