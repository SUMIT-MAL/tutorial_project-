from app.src.deepagent_ai import AgentStatergy
from pyresilience import resilient, TimeoutConfig, RetryConfig
from app.utils.helper import AiErrorHandeler


class AgentClient:
    """
    AgentClient is a wrapper class that manages the execution of an agent strategy.
    It takes an instance of a class that implements the AgentStatergy interface and provides methods to run the agent.
    Attributes:
        strategy (AgentStatergy): An instance of a class that implements the AgentStatergy interface.
    Methods:
        run_agent(query: str): Executes the agent strategy in a resilient manner and yields parsed chunks of the response.
        run_async_agent(query: str): Executes the agent strategy asynchronously in a resilient manner and returns the response.
    """

    def __init__(self, strategy: AgentStatergy):
        self._strategy = strategy

    @resilient(
        timeout=TimeoutConfig(
            seconds=100
        ),
        retry=RetryConfig(
            max_attempts=3
        )
    )
    async def run_agent(self, query: str):
        try:
            async for parsed_chunk in self._strategy.run_agent(query):
                yield parsed_chunk
        except AiErrorHandeler as error:
            yield {"error": str(error)}

    @resilient(
        timeout=TimeoutConfig(
            seconds=100
        ),
        retry=RetryConfig(
            max_attempts=3
        )
    )
    async def run_async_agent(self, query):
        try:
            response = await self._strategy.run_async_agent(query)
            return response
        except AiErrorHandeler as error:
            return {"error": str(error)}

    @resilient(
        timeout=TimeoutConfig(
            seconds=100
        ),
        retry=RetryConfig(
            max_attempts=3
        )
    )
    async def async_mcp_agent(self, query):
        try:
            async for chunk in self._strategy.mcp_agent_run(query):
                yield chunk
        except AiErrorHandeler as error:
            yield {"error": str(error)}
