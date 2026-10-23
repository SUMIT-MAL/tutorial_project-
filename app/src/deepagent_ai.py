from managed_deepagents import define_deep_agent, define_memory, MemoryLayer
from app.tools.tools_hub import image_search_thread, shoping_link_search_thread, description_search_thread
from langgraph.checkpoint.memory import InMemorySaver
from app.utils.helper import AiErrorHandeler
from loguru import logger
from langchain.mcp import MCPAdapter
from uuid import uuid4
from typing import AsyncIterator, Any
from deepagents import create_deep_agent
from abc import ABC, abstractmethod
from langchain_groq.chat_models import ChatGroq
import yaml


class AgentStatergy(ABC):
    """
    Abstract base class for defining agent strategies.
    This class provides an interface for implementing different agent strategies.
    Methods:
        run_agent(query: str): Executes the agent strategy in a resilient manner and yields parsed chunks of the response.
        run_async_agent(query: str): Executes the agent strategy asynchronously in a resilient manner and returns the response.
    """
    @abstractmethod
    async def run_agent(self):
        pass

    @abstractmethod
    async def run_async_agent(self):
        pass

    @abstractmethod
    async def mcp_agent_run(self):
        pass


class DeepAgentClient(AgentStatergy):
    """
    DeepAgentClient is a wrapper class that manages the execution of a deep agent.
    It takes an API key and model name as parameters and provides methods to run the agent.
    Attributes:
        api_key (str): The API key for the deep agent.
        model_name (str): The name of the model to be used by the deep agent.
    Methods:
        run_agent(query: str): Executes the deep agent in a resilient manner and yields parsed chunks of the response.
        run_async_agent(query: str): Executes the deep agent asynchronously in a resilient manner and returns the response.
    """

    def __init__(self, api_key: str, model_name: str):
        def prompt_parser() -> str:
            with open(file="prompt.yml", mode='r') as file:
                prompt = yaml.safe_load(file)
                return prompt["agent_config"]["system_prompt"]

        ai_prompt = prompt_parser()
        memory_object = InMemorySaver()

        self.agent = create_deep_agent(
            model=ChatGroq(
                model=model_name,
                api_key=api_key,
                temperature=0.0
            ),
            tools=[
                image_search_thread, shoping_link_search_thread, description_search_thread
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
                    "thread_id": str(uuid4())
                    }
                },
                stream_mode="messages",
                debug=True
            ):
                if isinstance(chunks, dict):
                    yield chunks.get("messages", {}).get("content", "")
                else:
                    yield chunks
        except Exception as error:
            logger.error(f"Error in running deep agent client: {error}")
            yield AiErrorHandeler("client is not working for now please try again later")

    async def run_async_agent(self, query: str):
        try:
            respones = await self.agent.ainvoke(
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
                        "thread_id": str(uuid4())
                    }
                },
                stream_mode="messages",
                debug=True
            )
            if isinstance(respones, dict):
                return respones.get("messages", {}).get("content", "")
            else:
                return respones
        except Exception as error:
            logger.error(f"Error in running deep agent client: {error}")
            return AiErrorHandeler("client is not working for now please try again later")

    async def mcp_agent_run(self):
        pass


class McpAgentClient(AgentStatergy):
    def __init__(self, model_name, api_key):
        self.model_name = model_name
        self.api_key = api_key

    async def mcp_agent_run(self, query):
        try:
            ################################
            'mcp agent'
            ################################
            config = {
                "shopping": {
                    "transport": "stdio",
                    "command": "uv",
                    "args": [
                        "run",
                        "--directory",
                        r"C:\Users\shova\Desktop\project\pc_bulider_sumit\shopping-mcp",
                        "shopping-mcp",
                    ],
                }
            }
            async with MCPAdapter(config) as mcp_adapter:
                tools = await mcp_adapter.list_tools()
                logger.warning(f"this is the mcp tools to use{tools}")
                self.mcp_agent = create_deep_agent(
                    model=ChatGroq(
                        model=self.model_name,
                        api_key=self.api_key,
                        temperature=0.0
                    ),
                    tools=tools,
                    checkpointer=InMemorySaver(),
                    system_prompt="You are a helpful assistant that can provide information about shopping, image search, and description search."
                )

            async for chunk in self.mcp_agent.astream(
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
                        "thread_id": str(uuid4())
                    }
                },
                stream_mode="messages",
                debug=True
            ):
                if isinstance(chunk, dict):
                    yield chunk.get("messages", {}).get("content", "")
                else:
                    yield chunk
        except Exception as error:
            logger.error(f"Error in running mcp agent: {error}")
            yield AiErrorHandeler("mcp agent is not working for now please try again later")

    async def run_agent(self):
        pass

    async def run_async_agent(self):
        pass
