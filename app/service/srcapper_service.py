from loguru import logger
from utils import WebsiteSrapperErrorHandeler
from client import SecraperService
from pyresilience import resilient, TimeoutConfig, RetryConfig
from fastapi.exceptions import HTTPException


@resilient(
    timeout=TimeoutConfig(
        seconds=20
    ),
    retry=RetryConfig(
        max_attempts=3
    )
)
async def scrape_pc_parts(client: SecraperService, parts: list[str]):
    """
        Scrapes PC parts using the provided client.

        Args:
            client (SracperClient): An instance of a scraper client (either ApifyPcPartPicker or PcPartsPicker).
        Returns:
            A list of search results from the respective platform.
      """
    try:
        async for result in client.scrape_pc_parts(parts):
            logger.info(f"this{parts}srapped sucessfully")
            yield result
    except WebsiteSrapperErrorHandeler as error:
        logger.error(f"can't parse the {parts}")
        raise HTTPException(detail=str(error))
