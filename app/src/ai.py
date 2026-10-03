from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph
from langchain_groq.chat_models import ChatGroq
from app.src.excutable_fuction import tool_excute
from app.utils import AiErrorHandeler
from loguru import logger

from app.config import seetings_manager


class AiAgentManger:
    def __init__(self):
        """
        Initializes the AiAgentManger class.
        This class is responsible for managing the AI agent that interacts with the PcPartsPicker tool.
        """

        self.logger = logger
        self.llm = ChatGroq(
            model=seetings_manager.model_agent,
            temperature=0.0,  # Set this to 0 for strict, deterministic tool execution
            api_key=seetings_manager.GROQ_API_KEY
        )
        self.agent_object: CompiledStateGraph = create_agent(
            model=self.llm,
            tools=[tool_excute],
            debug=True
        )
        self.logger.warning(
            "debug is true agent corrently running in developement mode")

    async def run_agent(self, user_input: str):
        """
        Runs the AI agent with the provided user input.

        """
        try:
            async for chenkes in self.agent_object.astream(
                input=user_input
            ):
                self.logger.info("checkig if client giving a string value")
                yield chenkes
        except Exception as error:
            self.logger.error(f"Error in run_agent: {error}")
            raise AiErrorHandeler(error)
