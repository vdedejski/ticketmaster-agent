import chainlit as cl
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import Runnable
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition

from src.models.state import State
from src.services.runnable import get_assistant_runnable
from src.services.tools.ticketmaster import tools
from src.services.tools.utils.tool_node import create_tool_node_with_fallback

assistant_runnable = get_assistant_runnable()

@cl.on_chat_start
async def on_chat_start():
    # start graph
    builder = StateGraph(State)
    builder.add_node("assistant", assistant_runnable)
    builder.add_node("tools", create_tool_node_with_fallback(tools))

    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    builder.add_edge("tools", "assistant")
    graph = builder.compile()

    state = State(messages=[])

    cl.user_session.set("graph", graph)
    cl.user_session.set("state", state)


@cl.on_message
async def on_message(message: cl.Message):
    graph: Runnable = cl.user_session.get("graph")

    state = cl.user_session.get("state")
    state["messages"] += [HumanMessage(content=message.content)]
    ui_message = cl.Message(content="")

    await ui_message.send()
    async for event in graph.astream_events(state, version="v1"):
        if event["event"] == "on_chat_model_stream" and event["name"] == "ChatOpenAI":
            content = event["data"]["chunk"].content or ""
            await ui_message.stream_token(token=content)
    await ui_message.update()

    state['messages'] += [AIMessage(content=ui_message.content)]