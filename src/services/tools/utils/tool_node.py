from src.services.tools.exceptions.error import handle_tool_error

from langgraph.prebuilt import ToolNode
from langchain_core.runnables import RunnableLambda

def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )