from app.src import SracperClient
from loguru import logger
from app.utils import WebsiteSrapperErrorHandeler
from fastapi.exceptions import HTTPException


class SecraperService:
    """
    This class provides a service for scraping PC parts using different scraper clients.
    It utilizes the resilient decorator to handle timeouts and retries for the scraping operations.
    """

    def __init__(self, client: SracperClient):
        """
        Initializes the SecraperService with a specific scraper client.

        Args:
            client (SracperClient): An instance of a scraper client (either ApifyPcPartPicker or PcPartsPicker).
        """
        self.client = client

    async def scrape_pc_parts(self, parts: list[str]):
        """
        Scrapes PC parts using the provided client.

        Args:
            client (SracperClient): An instance of a scraper client (either ApifyPcPartPicker or PcPartsPicker).
        Returns:
            A list of search results from the respective platform.
        """
        try:
            resault = await self.client.search_for_parts(
                parts=parts
            )
            logger.info(f"this{parts}srapped sucessfully")
            return resault
        except WebsiteSrapperErrorHandeler as error:
            logger.error(f"can't parse the {parts}")
            raise HTTPException(status_code=403, detail=str(error))
