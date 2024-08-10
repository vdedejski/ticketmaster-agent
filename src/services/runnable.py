from langchain_core.runnables import Runnable

from src.models.state import Assistant
from src.repository.llm import llm
from src.repository.prompts import primary_assistant_prompt
from src.services.tools.ticketmaster import tools

def get_assistant_runnable():
    chain: Runnable = primary_assistant_prompt | llm.bind_tools(tools)

    return Assistant(chain)

