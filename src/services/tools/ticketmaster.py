from langchain.tools import tool


@tool("flight_time")
def flight_time(hours: int) -> str:
    """Use this tool to answer what time a flight is."""
    return "Your flight is at 17PM CEST."

tools = [flight_time]