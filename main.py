import ast
from fastapi import FastAPI
from app.client.agent_base_runner import AgentClient
import json
import aiohttp
from app.src.deepagent_ai import McpAgentClient
from dotenv import load_dotenv
from app.helper.extract_pc_bulid import extract_pc_build
from app.config.settings import seetings_manager
from fastapi.responses import JSONResponse, StreamingResponse

app = FastAPI()
load_dotenv()

"""service = AgentClient(
    strategy=DeepAgentClient(
        api_key=seetings_manager.GROQ_API_KEY,
        model_name=seetings_manager.MODEL_NAME
    )
)
"""
mcp_agent_service = AgentClient(
    strategy=McpAgentClient(
        api_key=seetings_manager.GOOGLE_API_KEY,
        model_name=seetings_manager.MODEL_NAME
    )
)

"""
@app.post("/ai-respones")
async def agent_respones(query):
    This endpoint handles the AI response for a given query.
    It uses the AgentClient to run the agent and yield parsed chunks of the response.
    async for parsed_chunk in service.run_agent(query):
        yield parsed_chunk
"""


@app.post("/ai-mcp-respones")
async def agent_response(query: str):

    try:
        chunks = []

        async for parsed_chunk in mcp_agent_service.async_mcp_agent(
            query=query
        ):
            chunks.append(parsed_chunk)

        # Combine the collected results.
        raw = chunks

        # Search for the actual PC-build JSON.
        def extract_build(data):
            if isinstance(data, dict):
                if isinstance(data.get("parts"), list):
                    return data

                if data.get("type") == "text":
                    text = data.get("text", "")
                    if isinstance(text, str):
                        return extract_build(text)

                for value in data.values():
                    result = extract_build(value)
                    if result is not None:
                        return result

            elif isinstance(data, (list, tuple)):
                for item in data:
                    result = extract_build(item)
                    if result is not None:
                        return result

            elif isinstance(data, str):
                for parser in (json.loads, ast.literal_eval):
                    try:
                        parsed = parser(data)
                        result = extract_build(parsed)
                        if result is not None:
                            return result
                    except (ValueError, SyntaxError, TypeError):
                        continue

            return None

        build = extract_build(raw)

        if build is None:
            return JSONResponse(
                status_code=502,
                content={"error": "Could not extract PC build JSON"},
            )

        return JSONResponse(content=build)

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={"error": str(exc)},
        )

"""@app.post("/ai-respones-async")
async def async_agent_respones(query):
    
    This endpoint handles the AI response for a given query.
    It uses the AgentClient to run the agent and yield parsed chunks of the response.
    
    respones = await service.run_async_agent(query)
    return respones

"""
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
