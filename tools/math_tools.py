"""
math_tools.py
Mathematical operations for LangChain agents.
"""

from langchain.agents import Tool


def multiply(a: int, b: int) -> int:
    """Multiply two numbers.

    Args:
        a: first int
        b: second int
    """
    return a * b

def add(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a: first int
        b: second int
    """
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtract two numbers.

    Args:
        a: first int
        b: second int
    """
    return a - b

def divide(a: int, b: int) -> int:
    """Divide two numbers.

    Args:
        a: first int
        b: second int
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def modulus(a: int, b: int) -> int:
    """Get the modulus of two numbers.

    Args:
        a: first int
        b: second int
    """
    return a % b

def exponent(base: int, exp: int) -> int:
    """Calculate the exponent of a number.

    Args:
        base: base int
        exp: exponent int
    """
    return base ** exp

def square_root(num: int) -> float:

    """Calculate the square root of a number.

    Args:
        num: number int
    """
    if num < 0:
        raise ValueError("Cannot calculate square root of a negative number.")
    return num ** 0.5

def factorial(num: int) -> int:
    """Calculate the factorial of a number.

    Args:
        num: number int
    """
    if num < 0:
        raise ValueError("Cannot calculate factorial of a negative number.")
    if num == 0 or num == 1:
        return 1
    return num * factorial(num - 1)

def power(base: int, exp: int) -> int:
    """Calculate the power of a number.

    Args:
        base: base int
        exp: exponent int
    """
    return base ** exp

def logarithm(base: int, num: int) -> float:
    """Calculate the logarithm of a number.

    Args:
        base: base int
        num: number int
    """
    if base <= 0 or base == 1:
        raise ValueError("Base must be greater than 0 and not equal to 1.")
    if num <= 0:
        raise ValueError("Number must be greater than 0.")
    return math.log(num, base)

def absolute(num: int) -> int:
    """Calculate the absolute value of a number.

    Args:
        num: number int
    """
    return abs(num)

def percentage(part: int, whole: int) -> float:
    """Calculate the percentage of a part from a whole.

    Args:
        part: part int
        whole: whole int
    """
    if whole == 0:
        raise ValueError("Whole cannot be zero.")
    return (part / whole) * 100

def average(numbers: list[int]) -> float:
    """Calculate the average of a list of numbers.

    Args:
        numbers: list of numbers
    """
    if not numbers:
        raise ValueError("List cannot be empty.")
    return sum(numbers) / len(numbers)

def median(numbers: list[int]) -> float:
    """Calculate the median of a list of numbers.

    Args:
        numbers: list of numbers
    """
    if not numbers:
        raise ValueError("List cannot be empty.")
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
    return sorted_numbers[mid]

multiply_tool = Tool(
    name="multiply",
    func=multiply,
    description="Multiply two numbers. The numbers are a and b."
)

add_tool = Tool(
    name="add",
    func=add,
    description="Add two numbers."
)

subtract_tool = Tool(
    name="subtract",
    func=subtract,
    description="Subtract two numbers."
)

divide_tool = Tool(
    name="divide",
    func=divide,
    description="Divide two numbers."
)

modulus_tool = Tool(
    name="modulus",
    func=modulus,
    description="Get the modulus of two numbers."
)

exponent_tool = Tool(
    name="exponent",
    func=exponent,
    description="Calculate the exponent of a number."
)

square_root_tool = Tool(
    name="square_root",
    func=square_root,
    description="Calculate the square root of a number."
)

factorial_tool = Tool(
    name="factorial",
    func=factorial,
    description="Calculate the factorial of a number."
)

power_tool = Tool(
    name="power",
    func=power,
    description="Calculate the power of a number."
)

logarithm_tool = Tool(
    name="logarithm",
    func=logarithm,
    description="Calculate the logarithm of a number."
)

absolute_tool = Tool(
    name="absolute",
    func=absolute,
    description="Calculate the absolute value of a number."
)

percentage_tool = Tool(
    name="percentage",
    func=percentage,
    description="Calculate the percentage of a part from a whole."
)

average_tool = Tool(
    name="average",
    func=average,
    description="Calculate the average of a list of numbers."
)

median_tool = Tool(
    name="median",
    func=median,
    description="Calculate the median of a list of numbers."
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
        tools=[multiply_tool, add_tool, subtract_tool, divide_tool, modulus_tool,
               exponent_tool, square_root_tool, factorial_tool, power_tool,
               logarithm_tool, absolute_tool, percentage_tool, average_tool,
               median_tool],
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    # Example usage
    query = "What is the result of multiplying 5 and 3 ?"
    result = agent.invoke(query)
    print(result)
    query = "What is the result of adding 5 and 3 ?"
    result = agent.invoke(query)
    print(result)
    query = "What is the result of subtracting 5 from 3?"
    result = agent.invoke(query)
    print(result)
    query = "What is the result of dividing 5 by 3?"
    result = agent.invoke(query)
    print(result)
    query = "What is the result of getting the modulus of 5 and 3?"
    result = agent.invoke(query)
    print(result)
    query = "What is the result of calculating the exponent of 5 to the power of 3?"
    result = agent.invoke(query)
    print(result)
    query = "What is the result of calculating the square root of 25?"
    result = agent.invoke(query)
    print(result)
    query = "What is the result of calculating the factorial of 5?"
    result = agent.invoke(query)
    print(result)
    query = "What is the result of calculating the power of 5 to the power of 3?"
    result = agent.invoke(query)
    print(result)
    query = "What is the result of calculating the logarithm of 1000 to the base 10?"
    result = agent.invoke(query)
    print(result)
    query = "What is the result of calculating the absolute value of -5?"
    result = agent.invoke(query)
    print(result)
    query = "What is the result of calculating the percentage of 50 from 200?"
    result = agent.invoke(query)
    print(result)
    query = "What is the result of calculating the average of [1, 2, 3, 4, 5]?"
    result = agent.invoke(query)
    print(result)
    query = "What is the result of calculating the median of [1, 2, 3, 4, 5]?"
    result = agent.invoke(query)
    print(result)


