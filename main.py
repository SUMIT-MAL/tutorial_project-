from fastapi import FastAPI
from app.client.agent_base_runner import AgentClient
from app.src.deepagent_ai import DeepAgentClient
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

service = AgentClient(
    strategy=DeepAgentClient()
)


@app.post("/ai-respones")
async def agent_respones(query):
    """
    This endpoint handles the AI response for a given query.
    It uses the AgentClient to run the agent and yield parsed chunks of the response.
    """
    async for parsed_chunk in service.run_agent(query):
        yield parsed_chunk


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
