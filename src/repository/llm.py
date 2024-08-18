from langchain_openai import ChatOpenAI

from src.settings import settings

import os

llm = ChatOpenAI(model="gpt-4", 
                 openai_api_key=settings.OPENAI_API_KEY)
