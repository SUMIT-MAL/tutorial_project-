from loguru import logger
from app.utils import WebsiteSrapperErrorHandeler
from app.client import SecraperService
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
async def scrape_pc_parts(client: SecraperService, pc_parts: list[str]):
    """
        Scrapes PC parts using the provided client.

        Args:
            client (SracperClient): An instance of a scraper client (either ApifyPcPartPicker or PcPartsPicker).
        Returns:
            A list of search results from the respective platform.
      """
    try:
        result = await client.scrape_pc_parts(parts=pc_parts)
        logger.info(f"this{pc_parts}srapped sucessfully")
        return result
    except WebsiteSrapperErrorHandeler as error:
        logger.error(f"can't parse the {pc_parts}")
        raise RuntimeError(str(error))
