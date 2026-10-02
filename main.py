import asyncio
from app.service import run_agent

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

"""


async def main(inputs):
    async for chunk in run_agent(user_inputs=inputs):
        return chunk


if __name__ == "__main__":
    asyncio.run(
        main(inputs={"messages": [("user", "show me some best pc bulids")]}))
