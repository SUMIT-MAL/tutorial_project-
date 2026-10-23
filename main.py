from fastapi import FastAPI
from app.client.agent_base_runner import AgentClient
from app.src.deepagent_ai import DeepAgentClient, McpAgentClient
from dotenv import load_dotenv
from app.config.settings import seetings_manager
from fastapi.responses import JSONResponse
app = FastAPI()
load_dotenv()

service = AgentClient(
    strategy=DeepAgentClient(
        api_key=seetings_manager.GROQ_API_KEY,
        model_name=seetings_manager.MODEL_NAME
    )
)

mcp_agent_service = AgentClient(
    strategy=McpAgentClient(
        api_key=seetings_manager.GROQ_API_KEY,
        model_name=seetings_manager.MODEL_NAME
    )
)


@app.post("/ai-respones")
async def agent_respones(query):
    """
    This endpoint handles the AI response for a given query.
    It uses the AgentClient to run the agent and yield parsed chunks of the response.
    """
    async for parsed_chunk in service.run_agent(query):
        yield parsed_chunk


@app.post("/ai-mcp-respones")
async def agent_respones(query):
    """
    This endpoint handles the AI response for a given query.
    It uses the AgentClient to run the agent and yield parsed chunks of the response.
    """
    try:
        async for parsed_chunk in mcp_agent_service.async_mcp_agent(query):
            yield parsed_chunk
    except Exception as error:
        yield JSONResponse(
            status_code=500,
            content={"error": f"Error in running MCP agent: {error}"}
        )


@app.post("/ai-respones-async")
async def async_agent_respones(query):
    """
    This endpoint handles the AI response for a given query.
    It uses the AgentClient to run the agent and yield parsed chunks of the response.
    """
    respones = await service.run_async_agent(query)
    return respones


"""
source_client = SecraperService(client=PcPartsPicker())


async def main():
    result = await scrape_pc_parts(
        client=source_client,
        pc_parts=[
            'cpu',
            'mouse',
            'motherboard',
            'video-card',
        ]
    )
    return result


async def run():
    result = await main()
    print(result)

if __name__ == "__main__":
    asyncio.run(run())
"""
