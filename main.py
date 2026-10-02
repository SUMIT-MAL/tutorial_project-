from app.service import scrape_pc_parts
from app.client import SecraperService
from app.src import PcPartsPicker
import asyncio
from loguru import logger


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
