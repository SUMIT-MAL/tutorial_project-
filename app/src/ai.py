from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import InMemorySaver
from excutable_fuction import PcPartsPicker as ppp
from app.utils import AiErrorHandeler
from loguru import logger


class AiAgentManger:
    def __init__(self):
        """
        Initializes the AiAgentManger class.
        This class is responsible for managing the AI agent that interacts with the PcPartsPicker tool.
        """

        self.logger = logger
        self.agent_object: CompiledStateGraph = create_agent(
            model=None,
            tools=[ppp.tool_excute()],
            memory=InMemorySaver(),
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
                if isinstance(chenkes, str) == True:
                    yield chenkes
        except Exception as error:
            self.logger.error(f"Error in run_agent: {error}")
            raise AiErrorHandeler(str(errors=error))
