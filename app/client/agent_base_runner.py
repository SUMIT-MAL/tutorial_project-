from app.src.deepagent_ai import AgentStatergy
from pyresilience import resilient, TimeoutConfig, RetryConfig
from app.utils.helper import AiErrorHandeler


class AgentClient:
    def __init__(self, strategy: AgentStatergy):
        self._strategy = strategy

    @resilient(
        timeout=TimeoutConfig(
            seconds=20
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
