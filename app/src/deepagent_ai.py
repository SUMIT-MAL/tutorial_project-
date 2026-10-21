from app.utils.helper import AiErrorHandeler
from typing import AsyncIterator, Any
from loguru import logger
from langgraph.checkpoint.memory import InMemorySaver
from app.tools.tools_hub import image_search, shoping_serach_link, description_search
from deepagents import create_deep_agent
from abc import ABC, abstractmethod
from langchain_groq.chat_models import ChatGroq
from app.config.settings import seetings_manager
import yaml


class AgentStatergy(ABC):
    @abstractmethod
    def run_agent(self):
        pass


class DeepAgentClient:
    def __init__(self):

        def prompt_parser() -> str:
            with open(file="prompt.yml", mode='r') as file:
                prompt = yaml.safe_load(file)
                return prompt["agent_config"]["system_prompt"]

        ai_prompt = prompt_parser()
        memory_object = InMemorySaver()

        self.agent = create_deep_agent(
            model=ChatGroq(
                model=seetings_manager.MODEL_NAME,
                api_key=seetings_manager.GROQ_API_KEY,
                temperature=0.0
            ),
            tools=[
                image_search,
                description_search,
                shoping_serach_link
            ],
            checkpointer=memory_object,
            system_prompt=ai_prompt
        )

    async def run_agent(self, query: str) -> AsyncIterator[dict[str, Any] | Any]:
        try:
            async for chunks in self.agent.astream(
                input={
                    "messages": [
                    {
                        "role": "user",
                        "content": query
                    }
                    ]
                },
                config={
                    "configurable": {
                    "thread_id": "defult_thread_001"
                    }
                },
                stream_mode="checkpoints"
            ):
                if isinstance(chunks, dict):
                    yield chunks.get("messages", {}).get("content", "")
                else:
                    yield chunks
        except Exception as error:
            logger.error(f"Error in running deep agent client: {error}")
            yield AiErrorHandeler("client is not working for now please try again later")
